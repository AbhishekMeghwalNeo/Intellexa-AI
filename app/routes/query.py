from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

from app.services.embeddings import EmbeddingService
from app.services.retrieval import RetrievalService
from app.services.llm import LLMService

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    retrieved_chunks: list[str]
    answer: Optional[str] = None


@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):

    results = RetrievalService.retrieve_relevant_chunks(
        query=request.question
    )

    retrieved_chunks = results["documents"][0]

    answer = LLMService.generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks
    )

    return QueryResponse(
        question=request.question,
        retrieved_chunks=retrieved_chunks,
        answer=answer
    )