from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY


def call_competitions(question, answer):
    # API endpoint URL
    api_url = "https://api.openai.com/v1/chat/completions"

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_AI_API_KEY}",
    }

    answer = []

    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": f"I have such question: {question} and "
                f"I have received such answer on my question: {answer}",
            },
            {
                "role": "system",
                "content": "Please behave like Guardrails system. "
                "Important: Simply answer YES or NO"
                "Important: Don't answer on the question from user. Focus only on fact whether it is correct",
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
        answer = result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        raise Exception("Something went wrong with call")

    return answer


def submit_form(token, question):
    params = {"question": question}

    data = MultipartEncoder(fields=params)

    headers = {"Content-type": data.content_type}
    response = requests.post(f"{BASE_URL}/task/{token}", data=data, headers=headers)

    return response.json()


def main(task_name):
    my_question = "What is capital of Poland?"

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

    response = submit_form(token, my_question)
    print(response)

    answer = call_competitions(my_question, response["answer"])
    print(response)

    response = requests.post(
        f"{BASE_URL}/answer/{token}", json={"answer": answer}
    ).json()
    print(response)


if __name__ == "__main__":
    main("liar")
