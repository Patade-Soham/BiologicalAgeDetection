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

## Host It (Production)

This repo is now deployment-ready.

### Option 1: Render (Recommended)

1. Go to Render Dashboard -> `New` -> `Blueprint`.
2. Select this GitHub repo.
3. Render will detect `render.yaml` and create the service.
4. After deploy, open:
   - `https://<your-service>.onrender.com/health`
   - `https://<your-service>.onrender.com/docs`

### Option 2: Railway

1. Create a new Railway project from this GitHub repo.
2. Railway will use the `Dockerfile` / `railway.toml`.
3. Set env vars in Railway:
   - `APP_ENV=production`
   - `JWT_SECRET_KEY=<strong-secret>`
   - `DATABASE_URL=sqlite:///./data/lifespan_ai.db`
   - `UPLOAD_ROOT=./uploads`
4. Deploy and open `/health`.

### Option 3: Any Docker Host / VPS

```bash
docker build -t biological-age-api .
docker run -d -p 10000:10000 --name biological-age-api biological-age-api
```

Open `http://<server-ip>:10000/docs`.

## Pull model repos

```powershell
powershell -ExecutionPolicy Bypass -File scripts\fetch_github_models.ps1
```

## Important placeholder notes

- Model outputs for XGBoost, NN, cardio, metabolic, and GitHub adapters are deterministic heuristics for MVP scaffolding.
- Facial analysis currently uses a lightweight placeholder estimator.
- This gives you a complete tested product skeleton now, and clean extension points for plugging real model inference next.
