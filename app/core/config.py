from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Predictive Supply Chain Optimizer"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "supply_chain"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    
    DATABASE_URL: Optional[str] = None
    TEST_DATABASE_URL: Optional[str] = "postgresql+asyncpg://postgres:postgres@test_db:5433/supply_chain_test"

    JWT_SECRET_KEY: str = "yoursecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MODEL_PATH: str = "ml_models/supply_chain_model.joblib"
    MODEL_MODE: str = "mock"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
