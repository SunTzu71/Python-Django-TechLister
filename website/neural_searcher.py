from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-mpnet-base-v2", device="cpu")
        # initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url="https://a70aa4ee-b102-4f72-87bc-2d84095c40fd.us-east4-0.gcp.cloud.qdrant.io:6333",
            api_key="LBtuvaZRmX_kTUZJTTaj2D7DOqSl8DoipFBnMqWH9C16BC15u7MqlQ",
        )

    def search(self, text: str):
        # Convert text query into vector
        vector = self.model.encode(text).tolist()

        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=None,  # If you don't want any filters for now
            limit=5,
        )
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]

        return payloads
