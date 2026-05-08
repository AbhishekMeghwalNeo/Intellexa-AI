from pathlib import Path
from pypdf import PdfReader

class DocumentIngestionService:

    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> str:
        reader = PdfReader(file_path)
        extracted_text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

        return extracted_text.strip()
    
    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 100
    ) -> list[str]:

        chunks = []
        start = 0

        while start < len(text):

            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks