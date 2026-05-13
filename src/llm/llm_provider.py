from langchain_groq import ChatGroq
from src.config import settings
from langchain_openai import ChatOpenAI


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



class OpenAI_LLMProvider:
    _instance: ChatGroq | None = None

    @classmethod
    def get(cls) -> ChatGroq:
        if cls._instance is None:
            cls._instance = ChatOpenAI(
                base_url="",
                api_key="",
                model="gpt-5.4",
                temperature=0.0001,
                timeout=120,
                max_retries=5,
            )
        return cls._instance

