import traceback
from typing import List

import requests

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY


def call_competitions(strings: List[str]):
    # API endpoint URL
    api_url = "https://api.openai.com/v1/chat/completions"

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_AI_API_KEY}",
    }

    answer = []
    print(strings)

    counter = 0
    for string in strings:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": string},
                # {
                #     "role": "system",
                #     "content": "Make each fact as numbered points. Finish on 2.",
                # },
            ],
            "temperature": 0,
            "max_tokens": 250,
        }

        try:
            # Make the API request
            response = requests.post(
                api_url, json=payload, headers=headers, timeout=120
            )
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            result = response.json()
            answer.append(result["choices"][0]["message"]["content"])

            counter += 1
            print(f"Progress {counter}/{len(strings)}")
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            raise Exception("Something went wrong with call")

    return answer  # {"answer": answer}


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

    answer = call_competitions(response["blog"])

    response = requests.post(
        f"{BASE_URL}/answer/{token}", json={"answer": answer}
    ).json()

    print(response)


if __name__ == "__main__":
    main("blogger")
