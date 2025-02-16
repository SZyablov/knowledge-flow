from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from generator import (
    decide_how_to_answer, 
    extract_info,
    set_client
)
from text_processor import (
    preprocess_docs, 
    vectorize_docs, 
    index_vectors, 
    search_relevant_chunks
)
from config import (
    API_PROVIDER,
    DEBUG,
    HOST
)
from search import start_searching

from pydantic import BaseModel
import json
import traceback
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

set_client(API_PROVIDER)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[HOST],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    stream: str = True

@app.post("/ask")
async def ask_rag(request: QueryRequest):

    sum_time = 0
    start = datetime.now()

    print(f"Received request: {json.dumps(request.model_dump())}")
    query = request.query
    stream = request.stream

    try:
        decision = json.loads(
            decide_how_to_answer(query)
            .replace('```','')   # Подготовка сгенерированного текста
            .replace('json','')) # к конвертации в JSON 
        print('Запросы:\n' + '\n'.join(decision['queries']))
        
        # Поиск информации в источниках
        print("Начало поиска...")
        search_result = await start_searching(decision, query)
        print(f"Всего найдено: {len(search_result['retrieved_info'])} источников")

        end = datetime.now()
        sum_time += (end-start).total_seconds()
        print(f'🕑 Сбор данных за {(end-start).total_seconds():.2f} сек 🕑')
        start = datetime.now()

        # Разбитие всей полученной информации на чанки
        chunks = []
        text_to_chunk_mapping = []

        chunks, text_to_chunk_mapping = preprocess_docs(search_result)
        print(f"Всего чанков: {len(chunks)}")

        # Векторизация
        embeddings = vectorize_docs(chunks)
        print("Тексты векторизованы")

        # Индексация векторов
        index = index_vectors(embeddings)
        print("Векторы проиндексированы через FAISS")

        relevant_chunks, chunk_indices = search_relevant_chunks(
            decision['query_summary'], 
            index, 
            chunks, 
            embeddings)
        print(f"Найдено {len(relevant_chunks)} релевантных фрагментов")

        relevant = {}
        # Вывод информации о текстах, из которых взяты чанки
        for chunk, chunk_idx in zip(relevant_chunks, chunk_indices):
            text_id = text_to_chunk_mapping[chunk_idx]
            relevant[text_id] = chunk

        end = datetime.now()
        sum_time += (end-start).total_seconds()
        print(f'🕑 Обработка текстов за {(end-start).total_seconds():.2f} сек 🕑')
        start = datetime.now()

        if stream:
            return StreamingResponse(extract_info(relevant, query), media_type="text/plain")
        else:
            text = ''
            for chunk in extract_info(relevant, query):
                text += chunk
            return {"result": text}

        
    except:
        print(traceback.format_exc())