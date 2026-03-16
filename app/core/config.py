from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LIFESPAN AI"
    app_env: str = "development"
    database_url: str = "sqlite:///./lifespan_ai.db"
    jwt_secret_key: str = "change_me_please_super_secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    model_root: str = "./external_models"
    upload_root: str = "./uploads"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
