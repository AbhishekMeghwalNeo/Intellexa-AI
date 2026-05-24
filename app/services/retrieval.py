from app.services.embeddings import EmbeddingService
from app.vectorstore.chroma_manager import ChromaManager


class RetrievalService:

    @staticmethod
    def retrieve_relevant_chunks(
        query: str,
        top_k: int = 3
    ):

        query_embedding = (
            EmbeddingService.generate_embeddings([query])[0]
        )

        chroma_manager = ChromaManager()

        results = chroma_manager.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results