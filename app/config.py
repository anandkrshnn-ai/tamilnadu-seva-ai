import logging
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Setup logging pattern
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) - %(message)s"
)

logger = logging.getLogger("app.config")

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Model configuration
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # API Keys & Models
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "text-embedding-004"

    # API Server Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Local Path Config
    DATA_PATH: Path = BASE_DIR / "app" / "data" / "schemes_data.json"

settings = Settings()

if not settings.GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY is not set. The application will run in offline/mock mode.")
else:
    logger.info("Configuration successfully loaded. API Key validation completed.")
