from typing import List, Tuple
from uuid import uuid4

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import get_settings
from app.services.embedding_service import get_embeddings


def get_vectorstore(collection_name: str | None = None) -> Chroma:
    settings = get_settings()

    return Chroma(
        collection_name=collection_name or settings.chroma_collection_name,
        persist_directory=settings.chroma_persist_directory,
        embedding_function=get_embeddings(),
    )


def add_documents(documents: List[Document], collection_name: str | None = None) -> None:
    if not documents:
        return

    vectorstore = get_vectorstore(collection_name=collection_name)
    ids = [str(uuid4()) for _ in documents]
    vectorstore.add_documents(documents=documents, ids=ids)


def add_job_documents(documents: List[Document]) -> None:
    add_documents(documents=documents)


def similarity_search(
    query: str,
    k: int | None = None,
    collection_name: str | None = None,
) -> List[Tuple[Document, float]]:
    settings = get_settings()
    vectorstore = get_vectorstore(collection_name=collection_name)
    top_k = k or settings.top_k_results
    return vectorstore.similarity_search_with_relevance_scores(query, k=top_k)