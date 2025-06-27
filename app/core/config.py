from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_URL: AnyUrl
    DB_ECHO: bool = Field(default=False, env="DB_ECHO")  # type: ignore

    @property
    def async_db_uri(self) -> str:
        return str(self.DATABASE_URL)


settings = Settings()  # type: ignore
