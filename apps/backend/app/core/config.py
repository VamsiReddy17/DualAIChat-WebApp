from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator

# Root .env: app/core/config.py → app/core → app → backend → apps → project root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Dual AI Chat"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Azure AI Foundry — gpt-4o-mini
    AZURE_KEY: str | None = None
    AZURE_ENDPOINT: str | None = None
    AZURE_API_VERSION: str = "2024-12-01-preview"
    AZURE_DEPLOYMENT: str = "gpt-4o-mini"

    # Azure AI Foundry — DeepSeek-R1
    DEEPSEEK_ENDPOINT: str | None = None
    DEEPSEEK_API_KEY: str | None = None
    DEEPSEEK_DEPLOYMENT: str = "DeepSeek-R1"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=str(ENV_FILE),
        extra="ignore",
    )


settings = Settings()
