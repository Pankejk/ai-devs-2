import requests
from openai import OpenAI
from qdrant_client import QdrantClient

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY


def embed(string):
    client = OpenAI(
        api_key=OPEN_AI_API_KEY,
    )

    embeddings = client.embeddings.create(input=string, model="text-embedding-ada-002")
    return embeddings.model_dump()["data"][0]["embedding"]


def main(task_name):
    client = QdrantClient(host="localhost", port=6333)

    response = requests.post(
        f"{BASE_URL}/token/{task_name}", json={"apikey": API_KEY}
    ).json()
    try:
        token = response["token"]
    except Exception:
        print(response)
        raise
    response = requests.get(f"{BASE_URL}/task/{token}").json()
    question = response["question"]
    print(question)

    vector = embed(question)
    doc = client.search(query_vector=vector, limit=1, collection_name="news")
    print(doc)
    print(doc[0].model_dump()["payload"]["url"])

    response = requests.post(
        f"{BASE_URL}/answer/{token}",
        json={"answer": doc[0].model_dump()["payload"]["url"]},
    ).json()

    print(response)


if __name__ == "__main__":
    main("search")
