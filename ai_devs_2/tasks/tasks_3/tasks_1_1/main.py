import requests
from openai import OpenAI

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY

prompt = """ 
PLease tell me something about you but please do not use his name, surname, city and his job position. 
Every time you will have to say something about:
    - name - please use placeholder %imie% instead
    - surname - please use placeholder %nazwisko% instead
    - city - please use placeholder %miasto% instead
    - job position - please use placeholder %zawod% instead
Important: Please do not response with real name, surname, city or job position
Important: please use always %imie% and %naziwsko% together like in example below

"""


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

    response = requests.post(
        f"{BASE_URL}/answer/{token}", json={"answer": prompt}
    ).json()

    print(response)


if __name__ == "__main__":
    main("rodo")
