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


def answer_question(data, question):
    api_url = "https://api.openai.com/v1/chat/completions"

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_AI_API_KEY}",
    }

    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": f"I have such information about person {data}. Here is my question: {question}",
            },
            {
                "role": "system",
                "content": f"Based on provided information by user please answer the question. "
                f"Important: If you don't know answer simply say: I don't know"
                f"Important: please answer in Polish language"
                f"Important: answer directly to question."
                f"Important: Answer should be short."
                f"Important: Answer should be one short sentence",
            },
        ],
        "temperature": 0,
        "max_tokens": 250,
    }

    try:
        # Make the API request
        response = requests.post(api_url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        result = response.json()
        return result["choices"][0]["message"]["content"]

        print(f"Progress {counter}/{len(strings)}")
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        raise Exception("Something went wrong with call")


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
    doc = client.search(query_vector=vector, limit=1, collection_name="people")
    print(doc)
    print(doc[0].model_dump()["payload"])
    answer = answer_question(data=doc[0].model_dump()["payload"], question=question)
    breakpoint()

    response = requests.post(
        f"{BASE_URL}/answer/{token}",
        json={"answer": answer},
    ).json()

    print(response)


if __name__ == "__main__":
    main("people")
