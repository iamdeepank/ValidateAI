from email.policy import default

from pydantic_settings import BaseSettings
from pydantic import Field


class TableauSettings(BaseSettings):
    URL: str = Field(description="url of the dashboard.")

    HEADLESS: bool = Field(description="headless.",default=True)
    PAGE_LOAD_TIMEOUT:int = Field(description="headless.",default=120000)
    INITIAL_WAIT: int = Field(description="initial wait time.",default=10000)
    FILTER_WAIT: int = Field(description="filter wait.",default=2000)
    POST_FILTER_WAIT: int = Field(description="post filter wait.",default=5000)

    class Config:
        env_prefix = "TABLEAU_"