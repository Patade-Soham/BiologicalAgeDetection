# BiologicalAgeDetection - LIFESPAN AI MVP

This repository now contains a complete runnable MVP backend for biological age prediction based on your `project idea` documents.

## What is implemented

- FastAPI backend with versioned endpoints under `/api/v1`
- User auth: register, login, token-protected routes
- Lifestyle questionnaire submission and scoring
- Facial analysis upload endpoint (quality + facial age estimate)
- Biological age prediction endpoint with a 6-model ensemble
- Latest/history prediction endpoints
- SQLite persistence via SQLAlchemy
- Automated API tests with `pytest`

## External model integration

The project includes adapters for these GitHub models you listed:

- https://github.com/gitliber/AGE
- https://github.com/ina-foss/inaFaceAnalyzer

Current status:
- Adapter hooks are implemented in `app/services/model_service.py`
- If those repos are present in `external_models/AGE` and `external_models/inaFaceAnalyzer`, the app detects them.
- Exact inference wiring is still placeholder logic because each repo has its own runtime/contracts.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload
```

Open docs at: `http://127.0.0.1:8000/docs`

## Run tests

```bash
pytest -v
```

## Pull model repos

```powershell
powershell -ExecutionPolicy Bypass -File scripts\fetch_github_models.ps1
```

## Important placeholder notes

- Model outputs for XGBoost, NN, cardio, metabolic, and GitHub adapters are deterministic heuristics for MVP scaffolding.
- Facial analysis currently uses image-stat based placeholder estimation.
- This gives you a complete tested product skeleton now, and clean extension points for plugging real model inference next.
