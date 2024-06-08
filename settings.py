from typing import Optional, Self
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import RedisDsn, SecretStr, field_validator, model_validator


class Config(BaseSettings):
    bot_token: SecretStr
    session_storage: str
    redis_dsn: Optional[RedisDsn] = None
    database_name: Optional[str] = "statistics.db"
    win_gif: Optional[str] = None
    lose_gif: Optional[str] = None

    @field_validator("session_storage")
    @classmethod
    def validate_session_storage(cls, v: str) -> str:
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect 'session_storage' value")
        return v

    @model_validator(mode="after")
    def validate_redis_dsn(self) -> Self:
        if self.session_storage == "redis" and not self.redis_dsn:
            raise ValueError(
                "'session_storage' = 'redis', but 'redis_dsn' is missing"
            )
        return self

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

config = Config()
