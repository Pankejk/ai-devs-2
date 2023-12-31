import requests
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_data(url):
    return requests.get(url)


def answer_question(data, question):
    api_url = "https://api.openai.com/v1/chat/completions"

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_AI_API_KEY}",
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": question},
            {
                "role": "system",
                "content": f"Here is data: {data}. Please answer or user question based on it. "
                f"If there is no answer for question simply return I don't know."
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
    response = requests.post(
        f"{BASE_URL}/token/{task_name}", json={"apikey": API_KEY}
    ).json()
    try:
        token = response["token"]
    except Exception:
        print(response)
        raise

    response = requests.get(f"{BASE_URL}/task/{token}").json()

    data = get_data(response["input"])
    answer = answer_question(data, response["question"])

    response = requests.post(
        f"{BASE_URL}/answer/{token}", json={"answer": answer}
    ).json()

    print(response)


if __name__ == "__main__":
    main("scraper")
