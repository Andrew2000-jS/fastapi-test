import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    mongo_db_uri: str = Field(..., alias="MONGO_DB_URI")
    redis_url: str = Field(..., alias="REDIS_URL")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings() # type: ignore