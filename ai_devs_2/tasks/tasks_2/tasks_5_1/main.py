import requests
from openai import OpenAI

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY

add_user_function = {
    "name": "addUser",
    "description": "Add a user",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Provide user name",
            },
            "surname": {
                "type": "string",
                "description": "Provide surname",
            },
            "year": {
                "type": "integer",
                "description": "Provide birth year of the user",
            },
        },
    },
}


# def function_call():
#     client = OpenAI(
#         api_key=OPEN_AI_API_KEY,
#     )
#
#     response = client.completions.create(
#         model="gpt-3.5-turbo-16k",
#         message
#     )
#     return response


def main(task_name):
    response = requests.post(
        f"{BASE_URL}/token/{task_name}", json={"apikey": API_KEY}
    ).json()
    try:
        token = response["token"]
    except Exception:
        print(response)
        raise

    print(requests.get(f"{BASE_URL}/task/{token}").json())

    breakpoint()
    response = requests.post(
        f"{BASE_URL}/answer/{token}", json={"answer": add_user_function}
    ).json()

    print(response)


if __name__ == "__main__":
    main("functions")
