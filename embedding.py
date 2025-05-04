import requests, numpy as np
from config import EMBED_URL, EMBED_MODEL

def get_embedding(text: str) -> np.ndarray:
    res = requests.post(EMBED_URL, json={"model": EMBED_MODEL, "prompt": text})
    res.raise_for_status()
    return np.array([res.json()["embedding"]], dtype=np.float32)