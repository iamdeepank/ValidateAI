from langchain_groq import ChatGroq
from src.config import llm_settings


class LLMProvider:
    _instance: ChatGroq | None = None

    @classmethod
    def get(cls) -> ChatGroq:
        if cls._instance is None:
            cls._instance = ChatGroq(
                api_key=llm_settings.GROQ_API_KEY,
                model=llm_settings.MODEL,
                temperature=llm_settings.TEMPERATURE
            )
        return cls._instance
