from pathlib import Path
from pydantic_settings import BaseSettings
import logging
from pydantic import Field, computed_field
from redis.asyncio import Redis

BASE_DIR = Path(__file__).resolve().parent.__str__()
logger = logging.getLogger(__name__)



class Setting(BaseSettings):
    REDIS_URL: str = Field(
        json_schema_extra={"env": "REDIS_URL"},
        default="redis://localhost:6379/0"
    )
    DATABASE_URL: str = Field(
        json_schema_extra={"env": "DATABASE_URL"},
        default="postgresql+asyncpg://app_user:app_password@localhost:5432/app_db"
    )

    def __redis_client(self) -> Redis:
        _redis = Redis.from_url(self.REDIS_URL, decode_responses=True)
        return _redis

    @property
    def redis(self):
        return self.__redis_client()


settings = Setting()
