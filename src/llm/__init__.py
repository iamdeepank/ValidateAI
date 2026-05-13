from .llm_provider import LLMProvider,OpenAI_LLMProvider

# llm=LLMProvider.get()
llm=OpenAI_LLMProvider.get()

__all__=[
    "llm"
]