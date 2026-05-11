from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embeddings import EmbeddingService
from app.services.retrieval import RetrievalService
from app.services.llm import LLMService

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved_chunks: list[str]


@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):

    query_embedding = EmbeddingService.generate_query_embedding(request.question)

    retrieved_chunks = RetrievalService.retrieve_relevant_chunks(query_embedding=query_embedding,top_k=3)

    answer = LLMService.generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks
    )

    return QueryResponse(
        question=request.question,
        answer=answer,
        retrieved_chunks=retrieved_chunks
    )