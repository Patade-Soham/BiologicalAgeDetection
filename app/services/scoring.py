def compute_lifestyle_score(
    sleep_hours: float,
    exercise_days_per_week: int,
    stress_score: int,
    smoking_status: str,
    alcohol_drinks_per_week: int,
) -> float:
    sleep_component = max(0.0, 100.0 - abs(7.5 - sleep_hours) * 12.0)
    exercise_component = min(100.0, exercise_days_per_week * 14.0)
    stress_component = max(0.0, 100.0 - (stress_score / 40.0) * 100.0)

    smoking_penalty = 0.0
    if smoking_status == "former":
        smoking_penalty = 8.0
    elif smoking_status == "current":
        smoking_penalty = 25.0

    alcohol_penalty = min(20.0, alcohol_drinks_per_week * 0.8)

    raw = 0.3 * sleep_component + 0.3 * exercise_component + 0.4 * stress_component
    score = max(0.0, min(100.0, raw - smoking_penalty - alcohol_penalty))
    return round(score, 2)


def recommendations_from_inputs(lifestyle_score: float, stress_score: int, sleep_hours: float) -> list[str]:
    recs: list[str] = []
    if sleep_hours < 7.0:
        recs.append("Increase sleep to 7-8 hours with a fixed bedtime.")
    if stress_score > 18:
        recs.append("Add 15-20 minutes of daily stress management practice.")
    if lifestyle_score < 65:
        recs.append("Start with a 30-minute brisk walk 5 days per week.")
    if not recs:
        recs.append("Maintain current habits and repeat prediction next week.")
    return recs[:3]
