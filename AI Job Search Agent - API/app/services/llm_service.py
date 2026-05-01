from functools import lru_cache

from langchain_groq import ChatGroq

from app.core.config import get_settings


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    settings = get_settings()

    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.llm_model_name,
        temperature=0,
        max_tokens=settings.llm_max_tokens,
    )