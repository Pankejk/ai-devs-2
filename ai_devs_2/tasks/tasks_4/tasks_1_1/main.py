import json

import requests
from openai import OpenAI
from qdrant_client import QdrantClient

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY, MAKE_URL


def embed(string):
    client = OpenAI(
        api_key=OPEN_AI_API_KEY,
    )

    embeddings = client.embeddings.create(input=string, model="text-embedding-ada-002")
    return embeddings.model_dump()["data"][0]["embedding"]


def answer_question(question):
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
                "content": f"Here is my question: {question}",
            },
            {
                "role": "system",
                "content": f"Based on provided question. Please assign question to one of 3 categories: currency, "
                f"population and wide_knowledge"
                f"Important: If you don't know answer simply say: I don't know"
                f"Important: Don't answer directly to the question."
                f"Important: Answer should be short."
                f"Important: Answer should be json format"
                "Important: eg. {'choice': 'currency', 'currency': 'currency in question'}"
                "Important: eg. {'choice': 'population', 'country': 'cuntry taken from question'} in "
                "this case use english name of the country"
                "Important: eg. {'choice': 'wide_knowledge'}"
                "Important: in created json use double quotes instead ' ",
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
    print(response)

    question = response["question"]
    choice = answer_question(question=question)

    whole_data = {"question": response["question"], "data": json.loads(choice)}
    print(whole_data)
    response = requests.post(
        MAKE_URL,
        json=whole_data,
    ).json()

    answer = response[0] if isinstance(response, list) else response

    print(answer)

    response = requests.post(
        f"{BASE_URL}/answer/{token}",
        json=answer,
    ).json()

    print(response)

    # question = response["question"]
    # print(question)
    #
    # vector = embed(question)
    # doc = client.search(query_vector=vector, limit=1, collection_name="people")
    # print(doc)
    # print(doc[0].model_dump()["payload"])
    # answer = answer_question(data=doc[0].model_dump()["payload"], question=question)
    # breakpoint()
    #
    # response = requests.post(
    #     f"{BASE_URL}/answer/{token}",
    #     json={"answer": answer},
    # ).json()

    # print(response)


if __name__ == "__main__":
    main("knowledge")
