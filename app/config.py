from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_env: str = "development"
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.database_username}:{self.database_password}"
            f"@{self.database_hostname}:{self.database_port}/{self.database_name}"
        )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8-sig",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
