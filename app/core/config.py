from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_URL: AnyUrl
    DB_ECHO: bool = Field(default=False, env="DB_ECHO")  # type: ignore
    BACKEND_API_KEY: str = Field(..., env="BACKEND_API_KEY")  # type: ignore
    RESEND_API_KEY: str = Field(..., env="RESEND_API_KEY")  # type: ignore
    RESEND_FROM_EMAIL: str = Field(..., env="RESEND_FROM_EMAIL")  # type: ignore
    JWT_ACCESS_TOKEN_SECRET: str = Field(..., env="JWT_ACCESS_TOKEN_SECRET")  # type: ignore
    JWT_ACCESS_TOKEN_EXPIRATION: str = Field(default="30m", env="JWT_ACCESS_TOKEN_EXPIRATION")  # type: ignore
    JWT_REFRESH_TOKEN_SECRET: str = Field(..., env="JWT_REFRESH_TOKEN_SECRET")  # type: ignore
    JWT_REFRESH_TOKEN_EXPIRATION: str = Field(default="7d", env="JWT_REFRESH_TOKEN_EXPIRATION")  # type: ignore
    # FRONTEND_URL: str = Field(..., env="FRONTEND_URL")  # URL for password reset link

    @property
    def async_db_uri(self) -> str:
        return str(self.DATABASE_URL)


settings = Settings()  # type: ignore
