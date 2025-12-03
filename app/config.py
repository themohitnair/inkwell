"""Application configuration."""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
