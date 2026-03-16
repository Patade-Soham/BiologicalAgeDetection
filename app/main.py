from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import FacialAnalysis, Prediction, QuestionnaireResponse, User
from app.db.session import Base, engine, get_db
from app.schemas import (
    FacialAnalysisOut,
    HealthResponse,
    LoginRequest,
    MessageResponse,
    PredictionHistoryItem,
    PredictionRequest,
    PredictionResponse,
    QuestionnaireResponseOut,
    QuestionnaireSubmit,
    RegisterRequest,
    TokenResponse,
    UserProfile,
)
from app.services.auth import create_access_token, get_current_user, hash_password, verify_password
from app.services.image_service import ImageAnalysisError, save_and_analyze_image
from app.services.model_service import EnsemblePredictor, ModelContext
from app.services.scoring import compute_lifestyle_score, recommendations_from_inputs


Base.metadata.create_all(bind=engine)

app = FastAPI(title="LIFESPAN AI API", version="1.0.0")
predictor = EnsemblePredictor(model_root=settings.model_root)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", app=settings.app_name)


@app.post("/api/v1/auth/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        age=payload.age,
        gender=payload.gender,
        location=payload.location,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@app.get("/api/v1/users/me", response_model=UserProfile)
def get_me(current_user: User = Depends(get_current_user)):
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        age=current_user.age,
        gender=current_user.gender,
        location=current_user.location,
        created_at=current_user.created_at,
    )


@app.post("/api/v1/questionnaire/submit", response_model=QuestionnaireResponseOut)
def submit_questionnaire(
    payload: QuestionnaireSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    lifestyle_score = compute_lifestyle_score(
        sleep_hours=payload.sleep_hours,
        exercise_days_per_week=payload.exercise_days_per_week,
        stress_score=payload.stress_score,
        smoking_status=payload.smoking_status,
        alcohol_drinks_per_week=payload.alcohol_drinks_per_week,
    )

    response = QuestionnaireResponse(
        user_id=current_user.id,
        sleep_hours=payload.sleep_hours,
        exercise_days_per_week=payload.exercise_days_per_week,
        stress_score=payload.stress_score,
        smoking_status=payload.smoking_status,
        alcohol_drinks_per_week=payload.alcohol_drinks_per_week,
        notes=payload.notes,
        lifestyle_score=lifestyle_score,
    )
    db.add(response)
    db.commit()
    db.refresh(response)

    return QuestionnaireResponseOut(id=response.id, lifestyle_score=response.lifestyle_score, created_at=response.created_at)


@app.post("/api/v1/facial-analysis", response_model=FacialAnalysisOut)
def facial_analysis(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    content_type = image.content_type or ""
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    image_bytes = image.file.read()
    try:
        image_path, quality_score, facial_age_estimate = save_and_analyze_image(
            upload_bytes=image_bytes,
            upload_root=settings.upload_root,
            chronological_age=current_user.age,
        )
    except ImageAnalysisError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    record = FacialAnalysis(
        user_id=current_user.id,
        image_path=image_path,
        quality_score=quality_score,
        facial_age_estimate=facial_age_estimate,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return FacialAnalysisOut(
        analysis_id=record.id,
        quality_score=record.quality_score,
        facial_age_estimate=record.facial_age_estimate,
    )


@app.post("/api/v1/predict/biological-age", response_model=PredictionResponse)
def predict_biological_age(
    payload: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    latest_form = (
        db.query(QuestionnaireResponse)
        .filter(QuestionnaireResponse.user_id == current_user.id)
        .order_by(QuestionnaireResponse.created_at.desc())
        .first()
    )
    if latest_form is None:
        raise HTTPException(status_code=400, detail="Questionnaire is required before prediction")

    latest_face = (
        db.query(FacialAnalysis)
        .filter(FacialAnalysis.user_id == current_user.id)
        .order_by(FacialAnalysis.created_at.desc())
        .first()
    )

    facial_age = latest_face.facial_age_estimate if (payload.include_facial and latest_face) else None

    ctx = ModelContext(
        chronological_age=float(current_user.age),
        lifestyle_score=latest_form.lifestyle_score,
        stress_score=latest_form.stress_score,
        sleep_hours=latest_form.sleep_hours,
        exercise_days_per_week=latest_form.exercise_days_per_week,
        smoking_status=latest_form.smoking_status,
        alcohol_drinks_per_week=latest_form.alcohol_drinks_per_week,
        facial_age_estimate=facial_age,
    )

    result = predictor.predict(ctx)
    recs = recommendations_from_inputs(
        lifestyle_score=latest_form.lifestyle_score,
        stress_score=latest_form.stress_score,
        sleep_hours=latest_form.sleep_hours,
    )

    prediction = Prediction(
        user_id=current_user.id,
        chronological_age=result["biological_age"] - result["age_delta"],
        biological_age=result["biological_age"],
        age_delta=result["age_delta"],
        confidence_low=result["confidence_low"],
        confidence_high=result["confidence_high"],
        model_outputs_json=json.dumps(result["model_outputs"]),
        recommendations=" | ".join(recs),
        created_at=datetime.now(timezone.utc),
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return PredictionResponse(
        prediction_id=prediction.id,
        chronological_age=prediction.chronological_age,
        biological_age=prediction.biological_age,
        age_delta=prediction.age_delta,
        confidence_interval=[prediction.confidence_low, prediction.confidence_high],
        model_outputs=json.loads(prediction.model_outputs_json),
        recommendations=recs,
    )


@app.get("/api/v1/predictions/latest", response_model=PredictionResponse)
def latest_prediction(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .first()
    )
    if latest is None:
        raise HTTPException(status_code=404, detail="No predictions found")

    recs = [part.strip() for part in latest.recommendations.split("|") if part.strip()]

    return PredictionResponse(
        prediction_id=latest.id,
        chronological_age=latest.chronological_age,
        biological_age=latest.biological_age,
        age_delta=latest.age_delta,
        confidence_interval=[latest.confidence_low, latest.confidence_high],
        model_outputs=json.loads(latest.model_outputs_json),
        recommendations=recs,
    )


@app.get("/api/v1/predictions/history", response_model=list[PredictionHistoryItem])
def prediction_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    return [
        PredictionHistoryItem(id=row.id, biological_age=row.biological_age, age_delta=row.age_delta, created_at=row.created_at)
        for row in rows
    ]


@app.delete("/api/v1/users/me", response_model=MessageResponse)
def delete_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Prediction).filter(Prediction.user_id == current_user.id).delete()
    db.query(FacialAnalysis).filter(FacialAnalysis.user_id == current_user.id).delete()
    db.query(QuestionnaireResponse).filter(QuestionnaireResponse.user_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()
    return MessageResponse(message="Account and related data deleted")
