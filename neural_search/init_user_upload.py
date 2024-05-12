# Import client library
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from django.conf import settings
import numpy as np
import json

qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

# related vectors need to be added to a collection
qdrant_client.recreate_collection(
    collection_name="userlistings",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)

fd = open("./user_listings.json")

# payload is now an iterator over startup data
payload = map(json.loads, fd)

# Load all vectors into memory, numpy array works as iterable for itself.
# Other option would be to use Mmap, if you don't want to load all data into RAM
vectors = np.load("./user_listings.npy")

# upload data
qdrant_client.upload_collection(
    collection_name="userlistings",
    vectors=vectors,
    payload=payload,
    ids=None,  # Vector ids will be assigned automatically
    batch_size=256,  # How many vectors will be uploaded in a single request?
)
