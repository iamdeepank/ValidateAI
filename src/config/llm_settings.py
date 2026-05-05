from pydantic_settings import BaseSettings
from pydantic import Field

class LLMSettings(BaseSettings):
    GROQ_API_KEY:str= Field(description="Groq api key.")
    MODEL:str = Field(description="llm model name")
    TEMPERATURE:float = Field(description="temprature value of model.")

    class Config:
        env_prefix = "LLM_"
