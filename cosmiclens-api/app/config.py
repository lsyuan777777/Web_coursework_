"""
Application configuration settings
"""
import os
import secrets
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Settings:
    PROJECT_NAME: str = "CosmicLens API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days in minutes

    # Database type: 'sqlite' or 'postgresql'
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "sqlite")

    # SQLite settings
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "cosmiclens.db")

    # PostgreSQL settings (used if DATABASE_TYPE='postgresql')
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "cosmiclens")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")

    @property
    def DATABASE_URL(self) -> str:
        """Get database URL based on DATABASE_TYPE"""
        if self.DATABASE_TYPE == "sqlite":
            # Get absolute path for SQLite database
            db_path = Path(__file__).parent.parent / self.DATABASE_PATH
            return f"sqlite:///{db_path}"
        else:
            # PostgreSQL connection string
            return os.getenv(
                "DATABASE_URL",
                f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            )

settings = Settings()
