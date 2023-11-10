import traceback

import requests

from tasks.settings import BASE_URL, API_KEY


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

    try:
        secret = response["cookie"]
    except Exception:
        print(response)
        raise

    response = requests.post(
        f"{BASE_URL}/answer/{token}", json={"answer": secret}
    ).json()

    print(response)


if __name__ == "__main__":
    main("helloapi")
