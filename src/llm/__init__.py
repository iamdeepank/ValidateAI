from .groq_config import get_llm

llm=get_llm()

__all__=[
    "llm",
]