from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)
    age: int = Field(ge=18, le=100)
    gender: str
    location: str = ""


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class QuestionnaireSubmit(BaseModel):
    sleep_hours: float = Field(ge=0, le=16)
    exercise_days_per_week: int = Field(ge=0, le=14)
    stress_score: int = Field(ge=0, le=40)
    smoking_status: str = Field(pattern="^(never|former|current)$")
    alcohol_drinks_per_week: int = Field(ge=0, le=100)
    notes: str = ""


class QuestionnaireResponseOut(BaseModel):
    id: int
    lifestyle_score: float
    created_at: datetime


class PredictionRequest(BaseModel):
    include_facial: bool = True


class PredictionResponse(BaseModel):
    prediction_id: int
    chronological_age: float
    biological_age: float
    age_delta: float
    confidence_interval: List[float]
    model_outputs: Dict[str, float]
    recommendations: List[str]


class PredictionHistoryItem(BaseModel):
    id: int
    biological_age: float
    age_delta: float
    created_at: datetime


class FacialAnalysisOut(BaseModel):
    analysis_id: int
    quality_score: float
    facial_age_estimate: float


class UserProfile(BaseModel):
    id: int
    email: str
    age: int
    gender: str
    location: str
    created_at: datetime


class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str
    app: str
