from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import numpy as np
import json

#qdrant_client = QdrantClient("http://localhost:6333")
qdrant_client = QdrantClient(
    url="https://a70aa4ee-b102-4f72-87bc-2d84095c40fd.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key="LBtuvaZRmX_kTUZJTTaj2D7DOqSl8DoipFBnMqWH9C16BC15u7MqlQ",
)

qdrant_client.recreate_collection(
    collection_name="joblistings",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)

fd = open("./job_listings.json")
payload = map(json.loads, fd)
vectors = np.load("./job_listings.npy")

qdrant_client.upload_collection(
    collection_name="joblistings",
    vectors=vectors,
    payload=payload,
    ids=None,
    batch_size=256,
)
