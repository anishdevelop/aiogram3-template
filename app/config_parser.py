from typing import Optional

from pydantic import BaseSettings, BaseModel, SecretStr


class ConfigBot(BaseModel):
    token: SecretStr
    api: str = "https://api.telegram.org/"
    admin: int


class ConfigStorage(BaseModel):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    @property
    def redis_url(self) -> str:
        return (
            f"redis://{f'{self.redis_host}:{self.redis_password}@' if self.redis_password else ''}"
            f"{self.redis_host}:{self.redis_port}/{self.redis_db}"
        )


class ConfigWebhook(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    path: str = "/webhook"
    secret: Optional[SecretStr] = None


class ConfigDB(BaseModel):
    url: str


class Config(BaseSettings):
    bot: ConfigBot
    storage: ConfigStorage
    webhook: Optional[ConfigWebhook] = None
    db: ConfigDB

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
