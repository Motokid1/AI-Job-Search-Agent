from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="AI Job Search Agent", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="127.0.0.1", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    debug: bool = Field(default=True, alias="DEBUG")

    groq_api_key: str = Field(alias="GROQ_API_KEY")
    tavily_api_key: str = Field(alias="TAVILY_API_KEY")

    #openai/gpt-oss-120b
    llm_model_name: str = Field(default="llama-3.3-70b-versatile", alias="LLM_MODEL_NAME")
    embedding_model_name: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL_NAME",
    )


    chroma_persist_directory: str = Field(default="./chroma_db", alias="CHROMA_PERSIST_DIRECTORY")
    chroma_collection_name: str = Field(default="jobs_collection", alias="CHROMA_COLLECTION_NAME")
    chroma_analysis_collection_name: str = Field(
        default="analysis_collection",
        alias="CHROMA_ANALYSIS_COLLECTION_NAME",
    )
    chroma_resource_collection_name: str = Field(
        default="learning_resources_collection",
        alias="CHROMA_RESOURCE_COLLECTION_NAME",
    )
    chroma_job_match_collection_name: str = Field(
        default="job_match_collection",
        alias="CHROMA_JOB_MATCH_COLLECTION_NAME",
    )

    top_k_results: int = Field(default=10, alias="TOP_K_RESULTS")
    tavily_max_results: int = Field(default=8, alias="TAVILY_MAX_RESULTS")
    max_crawl_urls: int = Field(default=5, alias="MAX_CRAWL_URLS")
    max_analysis_market_results: int = Field(default=6, alias="MAX_ANALYSIS_MARKET_RESULTS")
    max_resource_results: int = Field(default=6, alias="MAX_RESOURCE_RESULTS")

    chunk_size: int = Field(default=1200, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=150, alias="CHUNK_OVERLAP")

    allowed_origins_raw: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        alias="ALLOWED_ORIGINS",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins_raw.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()