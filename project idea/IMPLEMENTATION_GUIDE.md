# LIFESPAN AI - IMPLEMENTATION GUIDE
## Step-by-Step Setup & Deployment (2026)

---

## 📦 QUICK START SETUP

### **1. Backend Setup (FastAPI + PostgreSQL)**

#### **Install Dependencies**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install packages
pip install fastapi uvicorn sqlalchemy psycopg2-binary redis python-jose
pip install xgboost scikit-learn tensorflow torch
pip install aiohttp python-multipart python-dotenv
pip install deepface opencv-python pillow
pip install anthropic  # Claude API
pip install pyodbc  # Database connection
```

#### **Environment Variables (.env)**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/lifespan_ai
REDIS_URL=redis://localhost:6379/0

# APIs
FITBIT_CLIENT_ID=your_fitbit_client_id
FITBIT_CLIENT_SECRET=your_fitbit_client_secret
GARMIN_CLIENT_ID=your_garmin_id
GARMIN_CLIENT_SECRET=your_garmin_secret
OURA_CLIENT_ID=your_oura_id
OURA_CLIENT_SECRET=your_oura_secret

# EPA AirNow
AIRNOW_API_KEY=your_airnow_key
GOOGLE_MAPS_API_KEY=your_google_maps_key

# Claude API
ANTHROPIC_API_KEY=your_anthropic_key

# AWS S3 (for facial images)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=lifespan-ai-images
AWS_REGION=us-east-1

# Security
JWT_SECRET_KEY=your_super_secret_key_min_32_chars
ENCRYPTION_KEY=your_encryption_key_base64_encoded

# Environment
ENVIRONMENT=development  # or production
DEBUG=False
```

---

### **2. Database Setup**

#### **PostgreSQL Installation & Setup**
```bash
# macOS
brew install postgresql

# Start PostgreSQL
brew services start postgresql

# Create database
createdb lifespan_ai

# Create tables (run SQL below)
psql lifespan_ai < schema.sql
```

#### **schema.sql** (Full schema provided in main spec)

---

### **3. Redis Setup** (for caching)

```bash
# macOS
brew install redis

# Start Redis
redis-server

# Test connection
redis-cli ping  # Should return "PONG"
```

---

### **4. ML Models Setup**

#### **Download Pretrained Models**
```python
# models/setup.py
import xgboost as xgb
import tensorflow as tf
from deepface import DeepFace
import os

# Create models directory
os.makedirs('models/pretrained', exist_ok=True)

# Initialize DeepFace (downloads on first use)
DeepFace.analyze(
    img_path="sample.jpg",
    actions=['age'],
    enforce_detection=False
)

# Load XGBoost model (train if needed)
# xgb_model = xgb.train(...)
# xgb_model.save_model('models/pretrained/xgboost_bio_age.bin')

# TensorFlow model loading
# keras_model = tf.keras.models.load_model('models/pretrained/nn_bio_age.h5')

print("✅ All models initialized")
```

#### **Train XGBoost Model**
```python
# models/train_xgboost.py
import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load training data (Korean Genome & Epidemiology Study format)
# Expected columns: 39 health features + chronological_age (target)
train_data = pd.read_csv('data/training_data.csv')

X = train_data.drop('chronological_age', axis=1)
y = train_data['chronological_age']

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.15, random_state=42
)

# Train XGBoost
params = {
    'n_estimators': 500,
    'max_depth': 6,
    'learning_rate': 0.01,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42,
    'objective': 'reg:squarederror'
}

model = xgb.XGBRegressor(**params)
model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    early_stopping_rounds=50,
    verbose=10
)

# Save
import joblib
joblib.dump(model, 'models/pretrained/xgboost_bio_age.pkl')
joblib.dump(scaler, 'models/pretrained/feature_scaler.pkl')

# Evaluate
from sklearn.metrics import mean_squared_error, r2_score
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.3f} years")
print(f"R²: {r2:.4f}")
```

---

### **5. API Server Setup**

#### **app/main.py** (FastAPI server)

```python
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import json

# Custom modules
from app.config import settings
from app.database import get_db, init_db
from app.models import (
    User, PredictionRequest, PredictionResponse,
    LifestyleProfile, VitalSigns
)
from app.services.ml import BioAgeEnsemble
from app.services.wearable import WearableAggregator
from app.services.auth import create_access_token, verify_token
from app.services.s3 import upload_image_s3, download_image_s3
from app.utils.encryption import encrypt_token, decrypt_token

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize models on startup
ml_models = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global ml_models
    logger.info("Loading ML models...")
    ml_models = BioAgeEnsemble.load_pretrained()
    await init_db()
    logger.info("✅ App started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="LIFESPAN AI API",
    version="1.0.0",
    description="Advanced biological aging prediction",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lifespan.ai", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== AUTHENTICATION ====================

@app.post("/api/v1/auth/register")
async def register(email: str, password: str, age: int, gender: str, db = Depends(get_db)):
    """Register new user"""
    
    # Check if user exists
    existing = await db.users.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_pwd = pwd_context.hash(password)
    
    # Create user
    user = {
        "email": email,
        "password_hash": hashed_pwd,
        "age": age,
        "gender": gender,
        "created_at": datetime.now(),
        "subscription_tier": "free"
    }
    
    result = await db.users.insert_one(user)
    
    # Create access token
    access_token = create_access_token(
        data={"user_id": str(result.inserted_id), "email": email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(result.inserted_id)
    }


@app.post("/api/v1/auth/login")
async def login(email: str, password: str, db = Depends(get_db)):
    """Login user"""
    
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    access_token = create_access_token(
        data={"user_id": str(user["_id"]), "email": user["email"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user["_id"])
    }


# ==================== CORE PREDICTIONS ====================

@app.post("/api/v1/predict/biological-age", response_model=PredictionResponse)
async def predict_biological_age(
    request: PredictionRequest,
    current_user = Depends(verify_token),
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Main prediction endpoint
    Combines 6 AI models into ensemble biological age
    """
    
    logger.info(f"Prediction request for user {current_user['user_id']}")
    
    try:
        # Fetch user data
        user = await db.users.find_one({"_id": current_user['user_id']})
        lifestyle = await db.lifestyle_profiles.find_one(
            {"user_id": current_user['user_id']}
        )
        vitals = await db.vital_signs.find_one(
            {"user_id": current_user['user_id']},
            sort=[("created_at", -1)]
        )
        
        # Get wearable data
        wearable_data = await fetch_wearable_aggregate(
            current_user['user_id'], 
            days=7,
            db=db
        )
        
        # Prepare feature vector
        features = prepare_feature_vector({
            'lifestyle': lifestyle.dict() if lifestyle else {},
            'vitals': vitals.dict() if vitals else {},
            'wearable': wearable_data,
            'user': {'age': user['age'], 'gender': user['gender']}
        })
        
        # Run predictions in parallel
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = {
                'xgboost': executor.submit(ml_models.predict_xgboost, features),
                'nn': executor.submit(ml_models.predict_neural_net, features),
                'facial': executor.submit(
                    get_facial_age, 
                    current_user['user_id'], 
                    db
                ),
                'cardiovascular': executor.submit(
                    ml_models.predict_cardio_age,
                    features
                ),
                'metabolic': executor.submit(
                    ml_models.predict_metabolic_age,
                    features
                )
            }
            
            # Also call Claude for LLM-based prediction
            health_report = generate_health_report(
                lifestyle, vitals, wearable_data, user
            )
            llm_pred = ml_models.predict_llm(health_report)
            
            # Collect results
            predictions = {
                'xgboost': futures['xgboost'].result(),
                'nn': futures['nn'].result(),
                'llm': llm_pred,
                'facial': futures['facial'].result(),
                'cardiovascular': futures['cardiovascular'].result(),
                'metabolic': futures['metabolic'].result()
            }
        
        # Ensemble
        ensemble_result = ml_models.ensemble(predictions)
        
        # Store in database
        prediction_doc = {
            'user_id': current_user['user_id'],
            'prediction_date': datetime.now(),
            **predictions,
            'final_biological_age': ensemble_result['biological_age'],
            'confidence_interval': ensemble_result['confidence_interval'],
            'age_delta': ensemble_result['age_delta'],
            'model_uncertainty': ensemble_result['model_uncertainty']
        }
        
        result = await db.biological_age_predictions.insert_one(prediction_doc)
        prediction_id = str(result.inserted_id)
        
        # Generate recommendations in background
        background_tasks.add_task(
            generate_recommendations,
            current_user['user_id'],
            prediction_id,
            ensemble_result,
            db
        )
        
        # Cache result
        import redis
        redis_client = redis.Redis.from_url(settings.REDIS_URL)
        redis_client.setex(
            f"user:{current_user['user_id']}:last_prediction",
            86400,  # 24 hours
            json.dumps(ensemble_result, default=str)
        )
        
        return PredictionResponse(
            **ensemble_result,
            prediction_id=prediction_id
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")


@app.post("/api/v1/facial-analysis")
async def analyze_facial_photo(
    image: UploadFile = File(...),
    current_user = Depends(verify_token),
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """Upload selfie for facial age analysis"""
    
    import hashlib
    import tempfile
    from deepface import DeepFace
    
    try:
        # Validate
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Must be image")
        
        # Read image
        image_bytes = await image.read()
        image_hash = hashlib.sha256(image_bytes).hexdigest()
        
        # Check duplicates
        existing = await db.facial_analysis.find_one({
            'user_id': current_user['user_id'],
            'image_hash': image_hash
        })
        
        if existing:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Duplicate image",
                    "analysis_id": str(existing['_id']),
                    "facial_age": existing.get('facial_age_estimate')
                }
            )
        
        # Upload to S3
        s3_key = f"facial/{current_user['user_id']}/{datetime.now().isoformat()}.jpg"
        await upload_image_s3(image_bytes, s3_key)
        
        # Analyze in background
        analysis_id = str(db.facial_analysis.insert_one({
            'user_id': current_user['user_id'],
            'photo_date': datetime.now(),
            'image_hash': image_hash,
            's3_bucket_key': s3_key,
            'status': 'processing'
        }).inserted_id)
        
        background_tasks.add_task(
            analyze_facial_async,
            current_user['user_id'],
            s3_key,
            analysis_id,
            db
        )
        
        return {
            "status": "processing",
            "analysis_id": analysis_id,
            "message": "Analyzing photo... results in 30-60 seconds"
        }
        
    except Exception as e:
        logger.error(f"Facial analysis error: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")


# ==================== WEARABLE INTEGRATION ====================

@app.post("/api/v1/wearable/connect/{device_type}")
async def connect_wearable(
    device_type: str,
    current_user = Depends(verify_token),
    db = Depends(get_db)
):
    """Start OAuth flow for wearable device"""
    
    valid_types = ['fitbit', 'garmin', 'oura', 'whoop', 'apple_health', 'google_fit']
    if device_type not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid device type")
    
    # Generate authorization URL
    auth_url = WearableAggregator.get_auth_url(
        device_type=device_type,
        user_id=current_user['user_id'],
        redirect_uri="https://api.lifespan.ai/api/v1/wearable/callback"
    )
    
    return {
        "auth_url": auth_url,
        "device_type": device_type
    }


@app.get("/api/v1/wearable/callback")
async def wearable_oauth_callback(
    code: str,
    state: str,
    device_type: str,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """Handle OAuth callback from wearable"""
    
    try:
        # Verify state (CSRF protection)
        user_id = await verify_oauth_state(state)
        
        # Exchange code for tokens
        tokens = await WearableAggregator.exchange_code(
            device_type=device_type,
            code=code
        )
        
        # Store encrypted tokens
        wearable_doc = {
            'user_id': user_id,
            'wearable_type': device_type,
            'access_token': encrypt_token(tokens['access_token']),
            'refresh_token': encrypt_token(tokens.get('refresh_token', '')),
            'token_expires_at': tokens.get('expires_at'),
            'sync_status': 'active',
            'last_sync': None,
            'created_at': datetime.now()
        }
        
        await db.wearable_sync.insert_one(wearable_doc)
        
        # Start initial sync
        background_tasks.add_task(
            sync_wearable_data,
            user_id=user_id,
            device_type=device_type,
            db=db
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "connected",
                "device_type": device_type,
                "message": "Device connected! Data syncing..."
            }
        )
        
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        raise HTTPException(status_code=400, detail="Connection failed")


# ==================== NEIGHBORHOOD MAPPER ====================

@app.get("/api/v1/neighborhood/aging-map")
async def get_neighborhood_aging_map(
    zip_code: str = None,
    current_user = Depends(verify_token),
    db = Depends(get_db)
):
    """Get neighborhood aging acceleration data"""
    
    if not zip_code:
        # Get from user profile
        user = await db.users.find_one({"_id": current_user['user_id']})
        zip_code = user.get('location_zip')
    
    # Get neighborhood stats (cached)
    import redis
    redis_client = redis.Redis.from_url(settings.REDIS_URL)
    
    cached = redis_client.get(f"neighborhood:{zip_code}:stats")
    if cached:
        neighborhood_stats = json.loads(cached)
    else:
        neighborhood_stats = await db.neighborhood_aging_stats.find_one({
            "zip_code": zip_code
        })
        redis_client.setex(
            f"neighborhood:{zip_code}:stats",
            604800,  # 7 days
            json.dumps(neighborhood_stats, default=str)
        )
    
    # Get environmental data
    env_data = await db.neighborhood_environment.find_one({
        "zip_code": zip_code
    })
    
    # User's own prediction for comparison
    user_pred = await db.biological_age_predictions.find_one(
        {"user_id": current_user['user_id']},
        sort=[("prediction_date", -1)]
    )
    
    return {
        "zip_code": zip_code,
        "neighborhood_stats": neighborhood_stats,
        "environmental_data": env_data,
        "your_comparison": {
            "your_age_delta": user_pred['age_delta'] if user_pred else None,
            "neighborhood_avg": neighborhood_stats.get('avg_age_delta') if neighborhood_stats else None,
            "difference_years": (
                user_pred['age_delta'] - neighborhood_stats['avg_age_delta']
            ) if user_pred and neighborhood_stats else None
        },
        "aging_factors": identify_key_factors(env_data),
        "recommendations": generate_neighborhood_recommendations(env_data)
    }


# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """API health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
```

---

### **6. Frontend Setup (React Native)**

#### **Install & Configure**
```bash
# Create React Native app
npx create-expo-app lifespan-ai
cd lifespan-ai

# Install dependencies
npm install @react-navigation/native @react-navigation/bottom-tabs
npm install react-native-paper react-native-gesture-handler
npm install axios react-native-chart-kit
npm install expo-health-connect expo-apple-health
npm install expo-camera expo-location

# Start dev server
npx expo start
```

#### **app.json Configuration**
```json
{
  "expo": {
    "name": "LIFESPAN AI",
    "slug": "lifespan-ai",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#6200ee"
    },
    "ios": {
      "supportsTabletMode": true,
      "infoPlist": {
        "NSHealthShareUsageDescription": "We need access to your health data",
        "NSHealthUpdateUsageDescription": "We need to save your health data",
        "NSCameraUsageDescription": "We need camera access for facial age analysis"
      }
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#6200ee"
      }
    },
    "plugins": [
      ["expo-health-connect", {}],
      ["expo-apple-health", {}],
      "expo-camera",
      "expo-location"
    ]
  }
}
```

---

### **7. Environment-specific Deployment**

#### **Docker Setup (Production)**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **docker-compose.yml**
```yaml
version: '3.9'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://lifespan:password@db:5432/lifespan_ai
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./models:/app/models

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=lifespan
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=lifespan_ai
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

#### **Deploy**
```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f api

# Stop
docker-compose down
```

---

### **8. Monitoring & Logging**

```python
# app/monitoring.py
import logging
from pythonjsonlogger import jsonlogger
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

# Initialize Sentry for error tracking
sentry_sdk.init(
    dsn="your_sentry_dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1
)

# JSON logging for ELK Stack
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

---

### **9. Testing**

```python
# tests/test_predictions.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_request():
    return {
        "sleep_hours_avg": 7.5,
        "exercise_frequency": 4,
        "stress_score": 5,
        "resting_hr": 62,
        "systolic_bp": 120,
        "diastolic_bp": 80
    }

def test_prediction_endpoint(sample_request):
    response = client.post(
        "/api/v1/predict/biological-age",
        json=sample_request,
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert "final_biological_age" in response.json()
    assert "age_delta" in response.json()
    assert "confidence_interval" in response.json()

def test_prediction_accuracy():
    """Test that ensemble RMSE < 2.5 years"""
    # Load test dataset
    # Run predictions
    # Assert RMSE < 2.5
    pass

def test_wearable_sync():
    """Test wearable data aggregation"""
    pass

def test_facial_analysis():
    """Test facial age prediction"""
    pass

# Run tests
# pytest tests/ -v
```

---

### **10. CI/CD Pipeline (GitHub Actions)**

```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: password
          POSTGRES_DB: lifespan_ai_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest tests/ --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: success()
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to AWS
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Deploy commands
          docker build -t lifespan-api:${{ github.sha }} .
          # Push to ECR
          # Update ECS service
```

---

## 🎯 QUICK REFERENCE: MOST CRITICAL SETUP STEPS

```bash
# 1. Database (mandatory)
createdb lifespan_ai
psql lifespan_ai < schema.sql

# 2. Redis (for caching)
redis-server

# 3. Install Python packages
pip install -r requirements.txt

# 4. Download ML models
python models/setup.py

# 5. Set environment variables
cp .env.example .env
# Edit .env with your API keys

# 6. Start API
python -m uvicorn app.main:app --reload

# 7. Start mobile app
cd mobile/
npx expo start

# ✅ Visit http://localhost:8000/docs (API docs)
# ✅ App available on phone/emulator
```

---

## 📊 PERFORMANCE TARGETS

| Component | Target | How to Achieve |
|-----------|--------|---|
| Prediction time | <2 seconds | Parallel model execution, caching |
| API response time (p95) | <500ms | Redis caching, DB indexing |
| Wearable sync uptime | >99.5% | Retry logic, health monitoring |
| ML model accuracy | ±2.5 years RMSE | Ensemble voting, hyperparameter tuning |
| Mobile app launch | <3 seconds | Code splitting, lazy loading |

---

**Ready to build? Start with:**
1. PostgreSQL + Redis setup
2. Clone the FastAPI skeleton
3. Configure environment variables
4. Run database migrations
5. Start developing! 🚀
