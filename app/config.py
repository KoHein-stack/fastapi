from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_env: str = "development"
    backend_cors_origins: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    railway_database_url: str | None = Field(default=None, validation_alias="DATABASE_URL")
    database_hostname: str | None = None
    database_port: str | None = None
    database_password: str | None = None
    database_name: str | None = None
    database_username: str | None = None
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @computed_field
    @property
    def database_url(self) -> str:
        if self.railway_database_url:
            return self.railway_database_url.replace("postgres://", "postgresql://", 1)

        missing_fields = [
            field_name
            for field_name in (
                "database_hostname",
                "database_port",
                "database_password",
                "database_name",
                "database_username",
            )
            if getattr(self, field_name) is None
        ]
        if missing_fields:
            missing = ", ".join(missing_fields)
            raise ValueError(f"Missing database settings: {missing}")

        return (
            f"postgresql://{self.database_username}:{self.database_password}"
            f"@{self.database_hostname}:{self.database_port}/{self.database_name}"
        )

    @computed_field
    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8-sig",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
