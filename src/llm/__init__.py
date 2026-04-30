from .llm_provider import LLMProvider

llm=LLMProvider.get()

__all__=[
    "llm",
]