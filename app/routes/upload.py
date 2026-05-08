from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.services.ingestion import DocumentIngestionService
from app.services.embeddings import EmbeddingService

router = APIRouter()

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf"]

# Pydantic model for the response of the upload endpoint
class UploadResponse(BaseModel):
    message: str
    filename: str
    extracted_text_preview: str
    total_chunks: int
    embedding_dimension: int

# Router Endpoitn for uploading documents
@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    unique_filename = f"{uuid4()}{file_extension}"

    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    extracted_text = (
        DocumentIngestionService.extract_text_from_pdf(file_path)
    )

    chunks = DocumentIngestionService.chunk_text(extracted_text)

    embeddings = EmbeddingService.generate_embeddings(chunks)

    return UploadResponse(
        message="File uploaded successfully",
        filename=unique_filename,
        extracted_text_preview=extracted_text[:500],
        total_chunks=len(chunks),
        embedding_dimension=len(embeddings[0]) if embeddings else 0
    )