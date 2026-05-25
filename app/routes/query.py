from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

from app.core.logger import logger

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

    logger.info("-----------------------------------------------------------------------------------")
    logger.info("QUERY Request received")
    logger.info(f"Received query: {request.question}")

    # Retrieve relevant chunks from the vector store based on the query 
    logger.info(f"Retrieving relevant chunks for query: {request.question}")
    results = RetrievalService.retrieve_relevant_chunks(
        query=request.question
    )

    retrieved_chunks = results["documents"][0]

    logger.info("Generating answer using the LLM service")
    answer = LLMService.generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks
    )

    logger.info(f"Query processed successfully. Answer generated: {answer}")

    logger.info("-----------------------------------------------------------------------------------")

    return QueryResponse(
        question=request.question,
        retrieved_chunks=retrieved_chunks,
        answer=answer
    )