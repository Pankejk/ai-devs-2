import traceback
from typing import List

import requests

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY


def are_responses_safe(strings: List[str]):
    # API endpoint URL
    api_url = "https://api.openai.com/v1/moderations"

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_AI_API_KEY}",
    }

    answer = []
    for string in strings:
        # Request payload
        payload = {"input": string}

        try:
            # Make the API request
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            result = response.json()
            if result["results"][0]["flagged"]:
                answer.append(1)
            else:
                answer.append(0)

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            raise Exception("Something went wrong with call")

    return answer


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

    answer = are_responses_safe(response["input"])
    response = requests.post(
        f"{BASE_URL}/answer/{token}", json={"answer": answer}
    ).json()

    print(response)


if __name__ == "__main__":
    main("moderation")
