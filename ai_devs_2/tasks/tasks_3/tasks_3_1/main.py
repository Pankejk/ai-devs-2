import requests
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY


def answer_question(data):
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
                "content": f"I am looking for a person. This all I know about this person: {data}",
            },
            {
                "role": "system",
                "content": f"Based on provided information by user please answer who use is describing. "
                f"Important: If you don't know who is this person simply answer: I don't know"
                f"Important: please answer in Polish language"
                f"Important: answer directly to question."
                f"Important: Answer should be short.",
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
    is_answered = False
    hints = []
    while not is_answered:
        response = requests.post(
            f"{BASE_URL}/token/{task_name}", json={"apikey": API_KEY}
        ).json()
        try:
            token = response["token"]
        except Exception:
            print(response)
            raise
        response = requests.get(f"{BASE_URL}/task/{token}").json()

        if not is_answered:
            hints.append(response["hint"])

        answer = answer_question(hints)

        print("Answer:", answer)
        print("Hints:", hints)
        if answer != "Nie wiem.":
            is_answered = True

    response = requests.post(
        f"{BASE_URL}/answer/{token}", json={"answer": answer}
    ).json()

    print(response)


if __name__ == "__main__":
    main("whoami")
