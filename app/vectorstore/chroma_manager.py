import chromadb
import uuid

class ChromaManager:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="document_chunks"
        )

    def add_documents(
        self,
        chunks: list[str],
        embeddings: list[list[float]]
    ):

        ids = [
            str(uuid.uuid4())
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3
    ):

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results
    

    