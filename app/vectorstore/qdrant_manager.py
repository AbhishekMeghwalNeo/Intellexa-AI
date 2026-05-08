# from qdrant_client import QdrantClient
# from qdrant_client.models import Distance, VectorParams
# from qdrant_client.models import PointStruct


# class QdrantManager:

#     COLLECTION_NAME = "document_chunks"

#     client = QdrantClient(
#         host="localhost",
#         port=6333
#     )

#     @classmethod
#     def create_collection(cls):

#         existing_collections = cls.client.get_collections()

#         collection_names = [
#             collection.name
#             for collection in existing_collections.collections
#         ]

#         if cls.COLLECTION_NAME not in collection_names:

#             cls.client.create_collection(
#                 collection_name=cls.COLLECTION_NAME,
#                 vectors_config=VectorParams(
#                     size=384,
#                     distance=Distance.COSINE
#                 )
#             )

#     @classmethod
#     def insert_embeddings(
#         cls,
#         chunks: list[str],
#         embeddings: list[list[float]]
#     ):

#         points = []

#         for idx, (chunk, embedding) in enumerate(
#             zip(chunks, embeddings)
#         ):

#             points.append(
#                 PointStruct(
#                     id=idx,
#                     vector=embedding,
#                     payload={
#                         "text": chunk
#                     }
#                 )
#             )

#         cls.client.upsert(
#             collection_name=cls.COLLECTION_NAME,
#             points=points
#         )