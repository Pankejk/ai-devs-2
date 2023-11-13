from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http.models import models, Batch
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Dict

import requests

from tasks.settings import OPEN_AI_API_KEY
from tasks.tasks_3.tasks_4_1.local_settings_ai import SQL_ALCHEMY_ENGINE
from tasks.tasks_3.tasks_4_1.models import NewsModel


def put_data_to_postgres(data: List[Dict]):
    with Session(SQL_ALCHEMY_ENGINE) as session:
        session.begin()
        new_data = []
        for item in data:
            obj = NewsModel(**item)
            breakpoint()
            new_data.append(obj.model_dump())
            try:
                session.add(obj)
            except:
                session.rollback()
                raise

        session.commit()
    return new_data


################################################################


def embed(string):
    client = OpenAI(
        api_key=OPEN_AI_API_KEY,
    )

    embeddings = client.embeddings.create(input=string, model="text-embedding-ada-002")
    return embeddings.model_dump()["data"][0]["embedding"]


def put_data_to_qdrant(data: List):
    collection_name = "news"
    data = [NewsModel(**item) for item in data]

    for item in data:
        item.vector = embed(item.info)

    client = QdrantClient(host="localhost", port=6333)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=1536, distance="Cosine", on_disk=True),
    )

    points = [item.vector for item in data]
    metadata = [
        {
            "title": item.title,
            "url": item.url,
            "info": item.info,
            "date": item.date,
            "id": item.id,
        }
        for item in data
    ]
    ids = [item.id for item in data]
    #
    client.upsert(
        collection_name=collection_name,
        wait=True,
        points=Batch(ids=ids, vectors=points, payloads=metadata),
    )


def get_data_from_source():
    return requests.get("https://unknow.news/archiwum.json").json()[:300]


def main():
    data = get_data_from_source()
    # data_with_id = put_data_to_postgres(data)
    put_data_to_qdrant(data)


if __name__ == "__main__":
    main()
