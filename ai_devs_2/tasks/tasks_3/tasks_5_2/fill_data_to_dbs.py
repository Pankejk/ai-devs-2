from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http.models import models, Batch
from typing import List, Dict

import requests

from tasks.settings import OPEN_AI_API_KEY
from tasks.tasks_3.tasks_5_2.models import PersonModel


################################################################


def embed(string):
    client = OpenAI(
        api_key=OPEN_AI_API_KEY,
    )

    embeddings = client.embeddings.create(input=string, model="text-embedding-ada-002")
    return embeddings.model_dump()["data"][0]["embedding"]


def put_data_to_qdrant(input_data: List):
    counter = 0
    size = 300

    client = QdrantClient(host="localhost", port=6333)

    collection_name = "people"
    # client.create_collection(
    #     collection_name=collection_name,
    #     vectors_config=models.VectorParams(size=1536, distance="Cosine", on_disk=True),
    # )

    tmp_data = input_data[1000:]

    for ind in range(0, len(tmp_data), size):
        data = tmp_data[ind : ind + size]

        data = [PersonModel(**item) for item in data]

        for item in data:
            item.vector = embed(
                f"Imie: {item.imie}, Nazwisko: {item.nazwisko}, Wiek: {item.wiek}, o_mnie: {item.o_mnie}, "
                f"ulubiona_postac_z_kapitana_bomby: {item.ulubiona_postac_z_kapitana_bomby}, "
                f"ulubiony_serial: {item.ulubiony_serial}, ulubiony_film: {item.ulubiony_film}, "
                f"ulubiony_kolor: {item.ulubiony_kolor}"
            )
            counter += 1
            print(f"progress of adding data: {counter}/{len(tmp_data)}")

        print("create point and metadata")
        points = [item.vector for item in data]
        metadata = [
            {
                "imie": item.imie,
                "nazwisko": item.nazwisko,
                "wiek": item.wiek,
                "o_mnie": item.o_mnie,
                "ulubiona_postac_z_kapitana_bomby": item.ulubiona_postac_z_kapitana_bomby,
                "ulubiony_serial": item.ulubiony_serial,
                "ulubiony_film": item.ulubiony_film,
                "ulubiony_kolor": item.ulubiony_kolor,
            }
            for item in data
        ]
        ids = [item.id for item in data]
        #
        print("inserting data")
        client.upsert(
            collection_name=collection_name,
            wait=True,
            points=Batch(ids=ids, vectors=points, payloads=metadata),
        )


def get_data_from_source():
    return requests.get("https://zadania.aidevs.pl/data/people.json").json()


def main():
    data = get_data_from_source()
    # data_with_id = put_data_to_postgres(data)
    put_data_to_qdrant(data)


if __name__ == "__main__":
    main()
