from sentence_transformers import SentenceTransformer

class EmbeddingService:

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    @classmethod
    def generate_embeddings(
        cls,
        chunks: list[str]
    ) -> list[list[float]]:

        embeddings = cls.model.encode(
            chunks,
            convert_to_numpy=True
        )

        return embeddings.tolist()
    
    @classmethod
    def generate_query_embedding(
        cls,
        query: str
    ) -> list[float]:

        embedding = cls.model.encode(
            query,
            convert_to_numpy=True
        )

        return embedding.tolist()