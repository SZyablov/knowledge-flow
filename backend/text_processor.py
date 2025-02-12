import re
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from config import CHUNK_SIZE, TOP_K, VECTORIZER_MODEL
from utils import sync_stopwatch

model = SentenceTransformer(VECTORIZER_MODEL, device="cpu")

# Функция для предобработки текста
@sync_stopwatch(description='docs preprocessing')
def preprocess_docs(docs):

    all_chunks = []
    text_to_chunk_mapping = []

    for text_id, text in docs['retrieved_info'].items():
        
        # Удаление лишних символов
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?]', '', text)
        text = text.lower()

        words = text.split()
        chunks = [' '.join(words[i:i + CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE)]

        all_chunks.extend(chunks)
        text_to_chunk_mapping.extend([text_id] * len(chunks))

    return all_chunks, text_to_chunk_mapping

# Функция для векторизации текста
@sync_stopwatch(description='docs vertorizing')
def vectorize_docs(chunks):
    embeddings = model.encode(chunks)
    return embeddings

# Функция для индексации векторов через FAISS
@sync_stopwatch(description='vector indexing')
def index_vectors(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

# Функция для поиска релевантных фрагментов
@sync_stopwatch(description='searching for relevant chunks')
def search_relevant_chunks(query, index, chunks, embeddings, top_k=TOP_K):
    n_samples, n_features = embeddings.shape
    n_components = min(n_samples, n_features, 128)
    pca = PCA(n_components=n_components)
    reduced_embeddings = pca.fit_transform(embeddings)

    # Создание оптимизированного индекса
    dimension = reduced_embeddings.shape[1]
    nlist = min(100, n_samples)
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_L2)

    # Обучение индекса
    index.train(reduced_embeddings)
    index.add(reduced_embeddings)

    # Поиск релевантных чанков
    query_embedding = model.encode([query])
    query_embedding_reduced = pca.transform(query_embedding)
    distances, indices = index.search(query_embedding_reduced, top_k)
    relevant_chunks = [chunks[idx] for idx in indices[0]]
    return relevant_chunks, indices[0]