from email.policy import default

from pydantic_settings import BaseSettings
from pydantic import Field

class DBSettings(BaseSettings):
    DB_URL:str= Field(description="local db",default="sqlite:///validateai.db")


    class Config:
        env_prefix = "DB_"