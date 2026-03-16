import io
import os

os.environ["DATABASE_URL"] = "sqlite:///./test_lifespan_ai.db"
os.environ["UPLOAD_ROOT"] = "./test_uploads"

from fastapi.testclient import TestClient

from app.db.models import FacialAnalysis, Prediction, QuestionnaireResponse, User
from app.db.session import Base, engine
from app.main import app


client = TestClient(app)


def _auth_header(email: str = "test@example.com", password: str = "Password123") -> dict[str, str]:
    register_payload = {
        "email": email,
        "password": password,
        "age": 30,
        "gender": "male",
        "location": "Pune",
    }
    client.post("/api/v1/auth/register", json=register_payload)
    login_response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module():
    engine.dispose()


def test_register_and_profile_flow():
    headers = _auth_header(email="user1@example.com")
    profile = client.get("/api/v1/users/me", headers=headers)

    assert profile.status_code == 200
    assert profile.json()["email"] == "user1@example.com"
    assert profile.json()["age"] == 30


def test_questionnaire_and_prediction_flow():
    headers = _auth_header(email="user2@example.com")

    form_payload = {
        "sleep_hours": 7.2,
        "exercise_days_per_week": 4,
        "stress_score": 14,
        "smoking_status": "never",
        "alcohol_drinks_per_week": 2,
        "notes": "good",
    }
    form_resp = client.post("/api/v1/questionnaire/submit", json=form_payload, headers=headers)
    assert form_resp.status_code == 200

    pred_resp = client.post("/api/v1/predict/biological-age", json={"include_facial": False}, headers=headers)
    assert pred_resp.status_code == 200

    body = pred_resp.json()
    assert "biological_age" in body
    assert "age_delta" in body
    assert "model_outputs" in body
    assert len(body["recommendations"]) >= 1

    latest = client.get("/api/v1/predictions/latest", headers=headers)
    history = client.get("/api/v1/predictions/history", headers=headers)
    assert latest.status_code == 200
    assert history.status_code == 200
    assert len(history.json()) == 1


def test_facial_analysis_flow():
    headers = _auth_header(email="user3@example.com")

    form_payload = {
        "sleep_hours": 6.0,
        "exercise_days_per_week": 1,
        "stress_score": 22,
        "smoking_status": "former",
        "alcohol_drinks_per_week": 8,
        "notes": "stressful",
    }
    client.post("/api/v1/questionnaire/submit", json=form_payload, headers=headers)

    # 1x1 png bytes
    png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\x99c``\x00\x00\x00\x04\x00\x01"
        b"\x0b\xe7\x02\x9d\x00\x00\x00\x00IEND\xaeB`\x82"
    )

    files = {"image": ("face.png", io.BytesIO(png), "image/png")}
    face_resp = client.post("/api/v1/facial-analysis", headers=headers, files=files)
    assert face_resp.status_code == 200
    assert "facial_age_estimate" in face_resp.json()

    pred_resp = client.post("/api/v1/predict/biological-age", json={"include_facial": True}, headers=headers)
    assert pred_resp.status_code == 200
    assert "facial" in pred_resp.json()["model_outputs"]


def test_requires_questionnaire_before_prediction():
    headers = _auth_header(email="user4@example.com")
    pred_resp = client.post("/api/v1/predict/biological-age", json={"include_facial": False}, headers=headers)
    assert pred_resp.status_code == 400
    assert "Questionnaire" in pred_resp.text
