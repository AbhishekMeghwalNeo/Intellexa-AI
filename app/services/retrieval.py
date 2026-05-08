import numpy as np

VECTOR_STORE = []

class RetrievalService:

    @staticmethod
    def store_embeddings(
        chunks: list[str],
        embeddings: list[list[float]]
    ):

        for chunk, embedding in zip(chunks, embeddings):
            VECTOR_STORE.append(
                {
                    "chunk": chunk,
                    "embedding": embedding
                }
            )
        return "Embeddings stored in vector database successfully"

    @staticmethod
    def cosine_similarity(vec1, vec2):

        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        return np.dot(vec1, vec2) / (
            np.linalg.norm(vec1) * np.linalg.norm(vec2)
        )

    @classmethod
    def retrieve_relevant_chunks(
        cls,
        query_embedding,
        top_k: int = 3
    ):

        similarities = []

        for item in VECTOR_STORE:

            similarity = cls.cosine_similarity(
                query_embedding,
                item["embedding"]
            )

            similarities.append(
                (
                    similarity,
                    item["chunk"]
                )
            )

        similarities.sort(
            key=lambda x: x[0],
            reverse=True
        )

        top_chunks = similarities[:top_k]

        return [chunk for _, chunk in top_chunks]