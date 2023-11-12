import requests
from openai import OpenAI

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY


def embed():
    client = OpenAI(
        api_key=OPEN_AI_API_KEY,
    )

    embeddings = client.embeddings.create(
        input="Hawaiian pizza", model="text-embedding-ada-002"
    )
    return embeddings.dict()["data"][0]["embedding"]


def main(task_name):
    response = requests.post(
        f"{BASE_URL}/token/{task_name}", json={"apikey": API_KEY}
    ).json()
    try:
        token = response["token"]
    except Exception:
        print(response)
        raise

    response = requests.get(f"{BASE_URL}/task/{token}").json()
    print(response)

    data = embed()

    response = requests.post(f"{BASE_URL}/answer/{token}", json={"answer": data}).json()

    print(response)


if __name__ == "__main__":
    main("embedding")
