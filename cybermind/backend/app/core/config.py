from typing import List, Optional, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import os

class Settings(BaseSettings):
    APP_NAME: str = "CyberMIND"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Secret Key (supports SECRET_KEY or JWT_SECRET)
    SECRET_KEY: str = Field(default="cybermind-super-secure-jwt-secret-key-change-in-production-2026")
    JWT_SECRET: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Host & Port for cloud platforms (Render, Railway, Fly.io, Cloud Run)
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database (PostgreSQL with pgvector for prod; SQLite for zero-setup demo)
    DATABASE_URL: str = Field(default="sqlite:///./cybermind.db")
    
    # Environment & Modes
    ENVIRONMENT: str = "development"  # "production" or "development"
    DEBUG: bool = False
    DEMO_MODE: bool = True  # In production, set DEMO_MODE=false to disable default demo seed
    
    # URLs
    FRONTEND_URL: Optional[str] = "http://localhost:3000"
    BACKEND_URL: Optional[str] = "http://localhost:8000"
    
    # Security & CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    
    # AI / LLM Configuration
    LLM_PROVIDER: str = "mock"  # "openai", "compatible", "mock"
    LLM_API_KEY: Optional[str] = ""
    OPENAI_API_KEY: Optional[str] = None  # alias for LLM_API_KEY
    LLM_API_BASE: Optional[str] = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Graph & Vector DB
    NEO4J_URI: Optional[str] = "bolt://localhost:7687"
    NEO4J_USERNAME: Optional[str] = "neo4j"
    NEO4J_PASSWORD: Optional[str] = "cybermind123"
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"
    
    # Blockchain
    BLOCKCHAIN_RPC_URL: Optional[str] = "http://localhost:8545"
    BLOCKCHAIN_PRIVATE_KEY: Optional[str] = ""

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def parse_database_url(cls, v):
        if isinstance(v, str) and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            # Supports comma-separated origins like "https://example.com,https://api.example.com"
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    def get_cors_origins(self) -> List[str]:
        origins = list(self.CORS_ORIGINS) if isinstance(self.CORS_ORIGINS, list) else [self.CORS_ORIGINS]
        if self.FRONTEND_URL and self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)
        if self.ENVIRONMENT == "production":
            # In production, restrict CORS strictly to remote custom origins if configured
            non_local = [o for o in origins if not ("localhost" in o or "127.0.0.1" in o)]
            if non_local:
                return non_local
        return origins

    def get_jwt_secret(self) -> str:
        return self.JWT_SECRET or self.SECRET_KEY

    def get_llm_key(self) -> str:
        return self.OPENAI_API_KEY or self.LLM_API_KEY or ""
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
