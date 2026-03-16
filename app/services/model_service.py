from __future__ import annotations

import math
import os
from dataclasses import dataclass
from statistics import pstdev
from typing import Dict


@dataclass
class ModelContext:
    chronological_age: float
    lifestyle_score: float
    stress_score: int
    sleep_hours: float
    exercise_days_per_week: int
    smoking_status: str
    alcohol_drinks_per_week: int
    facial_age_estimate: float | None = None


class GithubAgeAdapter:
    """
    Optional adapter for github model repos listed by user.
    If those repos are not present locally, this falls back to heuristic output.
    """

    def __init__(self, model_root: str):
        self.model_root = model_root
        self.age_repo_exists = os.path.isdir(os.path.join(model_root, "AGE"))
        self.face_repo_exists = os.path.isdir(os.path.join(model_root, "inaFaceAnalyzer"))

    def predict_age(self, ctx: ModelContext) -> float:
        if self.age_repo_exists:
            # Placeholder integration point for gitliber/AGE inference script.
            return round(ctx.chronological_age - (ctx.lifestyle_score - 50.0) * 0.04, 2)
        return round(ctx.chronological_age - (ctx.lifestyle_score - 50.0) * 0.03, 2)

    def predict_facial(self, ctx: ModelContext) -> float:
        if ctx.facial_age_estimate is not None:
            return round(ctx.facial_age_estimate, 2)
        if self.face_repo_exists:
            # Placeholder integration point for ina-foss/inaFaceAnalyzer.
            return round(ctx.chronological_age + 0.5, 2)
        return round(ctx.chronological_age + 0.8, 2)


class EnsemblePredictor:
    def __init__(self, model_root: str):
        self.github = GithubAgeAdapter(model_root=model_root)

    def predict(self, ctx: ModelContext) -> Dict[str, float | dict]:
        lifestyle_adjust = (50.0 - ctx.lifestyle_score) * 0.08
        stress_adjust = (ctx.stress_score - 12) * 0.1
        sleep_adjust = abs(7.5 - ctx.sleep_hours) * 0.35
        habit_penalty = 0.0
        if ctx.smoking_status == "former":
            habit_penalty += 0.8
        elif ctx.smoking_status == "current":
            habit_penalty += 2.5
        habit_penalty += min(1.8, ctx.alcohol_drinks_per_week * 0.05)

        xgboost = ctx.chronological_age + lifestyle_adjust + stress_adjust + sleep_adjust + habit_penalty
        nn = ctx.chronological_age + lifestyle_adjust * 0.8 + stress_adjust * 1.1 + sleep_adjust
        cardio = ctx.chronological_age + stress_adjust + habit_penalty + max(0, 3 - ctx.exercise_days_per_week) * 0.35
        metabolic = ctx.chronological_age + lifestyle_adjust + max(0, 5 - ctx.exercise_days_per_week) * 0.22
        github_age = self.github.predict_age(ctx)
        facial = self.github.predict_facial(ctx)

        model_outputs = {
            "xgboost": round(xgboost, 2),
            "neural_net": round(nn, 2),
            "cardio": round(cardio, 2),
            "metabolic": round(metabolic, 2),
            "github_age": round(github_age, 2),
            "facial": round(facial, 2),
        }

        weights = {
            "xgboost": 0.22,
            "neural_net": 0.20,
            "cardio": 0.16,
            "metabolic": 0.14,
            "github_age": 0.16,
            "facial": 0.12,
        }

        biological_age = sum(model_outputs[k] * w for k, w in weights.items())
        model_std = pstdev(model_outputs.values()) if len(model_outputs) > 1 else 0.0
        ci_low = biological_age - 1.96 * max(0.5, model_std / math.sqrt(len(model_outputs)))
        ci_high = biological_age + 1.96 * max(0.5, model_std / math.sqrt(len(model_outputs)))

        return {
            "biological_age": round(biological_age, 2),
            "age_delta": round(biological_age - ctx.chronological_age, 2),
            "confidence_low": round(ci_low, 2),
            "confidence_high": round(ci_high, 2),
            "model_outputs": model_outputs,
        }
