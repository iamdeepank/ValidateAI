from langchain_groq import ChatGroq
from src.config import settings


class LLMProvider:
    _instance: ChatGroq | None = None

    @classmethod
    def get(cls) -> ChatGroq:
        if cls._instance is None:
            cls._instance = ChatGroq(
                api_key=settings.llm.GROQ_API_KEY,
                model=settings.llm.MODEL,
                temperature=settings.llm.TEMPERATURE
            )
        return cls._instance
