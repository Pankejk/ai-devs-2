import datetime

import json

import requests
from openai import OpenAI
from qdrant_client import QdrantClient

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY, MAKE_URL


def embed(url):
    client = OpenAI(
        api_key=OPEN_AI_API_KEY,
    )

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What is colour of the hat that creature has on had on image?"
                        "Important: if creature is not a gnome return: ERROR. Important: "
                        "Simpy answer fo user question. Important: Simply return colour in polish language",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url,
                        },
                    },
                ],
            },
        ],
        max_tokens=300,
    )

    return response.choices[0].dict()["message"]["content"]


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

    response = requests.post(
        f"{BASE_URL}/answer/{token}",
        json={"answer": MAKE_URL},
    ).json()

    print(response)


if __name__ == "__main__":
    main("ownapi")
