import faiss
import redis
import numpy as np
from sentence_transformers import SentenceTransformer
from config import REDIS_HOST

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
model = model.to("cuda")

redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
index = faiss.read_index("embeddings/faiss_index.bin")

def search(desicion_result: dict):

    

    pass

def retrieve(query, top_k=5):
    query_embedding = model.encode([query])
    _, indices = index.search(np.array(query_embedding), top_k)
    
    results = []
    for idx in indices[0]:
        doc = redis_client.get(f"doc:{idx}")
        if doc:
            results.append(doc)
    
    return results
