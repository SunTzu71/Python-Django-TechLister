from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

model = SentenceTransformer(
    "all-mpnet-base-v2", device="cpu"
)  # or device="cpu" if you don't have a GPU

df = pd.read_json("./job_listings.json", lines=True)

vectors = model.encode(
    [str(row.id) + ". " + row.about for row in df.itertuples()],
    show_progress_bar=True,
)

vectors.shape
print('shape: ', vectors.shape)
# > (40474, 384)

np.save("job_listings.npy", vectors, allow_pickle=False)
