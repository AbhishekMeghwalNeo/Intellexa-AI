from fastapi import APIRouter
from typing import Optional

from pydantic import BaseModel

from app.core.logger import logger
from app.core.langfuse_config import langfuse

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

    # =========================
    # LANGFUSE TRACE START
    # =========================

    trace = langfuse.trace(
        name="rag-query",
        input={
            "question": request.question
        }
    )

    # =========================
    # RETRIEVAL STEP
    # =========================

    retrieval_span = trace.span(
        name="retrieval-step"
    )

    logger.info(
        f"Retrieving relevant chunks for query: {request.question}"
    )

    results = RetrievalService.retrieve_relevant_chunks(
        query=request.question
    )

    retrieved_chunks = results["documents"][0]

    retrieval_span.end(
        output={
            "retrieved_chunks": retrieved_chunks
        }
    )

    # =========================
    # LLM GENERATION STEP
    # =========================

    llm_span = trace.span(
        name="llm-generation"
    )

    logger.info("Generating answer using the LLM service")

    answer = LLMService.generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks
    )

    llm_span.end(
        output={
            "answer": answer
        }
    )

    # =========================
    # FINAL TRACE OUTPUT
    # =========================

    trace.update(
        output={
            "answer": answer
        }
    )

    logger.info("Query processed successfully.")
    logger.info("-----------------------------------------------------------------------------------")

    return QueryResponse(
        question=request.question,
        retrieved_chunks=retrieved_chunks,
        answer=answer
    )

