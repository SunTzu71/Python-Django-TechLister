from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from django.conf import settings
import numpy as np
import json

qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
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
