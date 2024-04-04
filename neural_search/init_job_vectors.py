from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

model = SentenceTransformer(
    "all-mpnet-base-v2", device="cpu"
)

df = pd.read_json("./job_listings.json", lines=True)
vectors = model.encode(
    [str(row.id) + ". " + row.about for row in df.itertuples()],
    show_progress_bar=True,
)

print('vector shape: ', vectors.shape)

np.save("job_listings.npy", vectors, allow_pickle=False)
