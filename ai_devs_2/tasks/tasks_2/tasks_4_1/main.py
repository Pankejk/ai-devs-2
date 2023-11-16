import os

import requests
from openai import OpenAI

from tasks.settings import BASE_URL, API_KEY, OPEN_AI_API_KEY


def transcript_data(data):
    client = OpenAI(
        api_key=OPEN_AI_API_KEY,
    )

    transcription = client.audio.transcriptions.create(model="whisper-1", file=data)
    return transcription.text


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
    file_url = f"https{response['msg'].split('https')[1]}"
    data = requests.get(file_url).content

    file_name = "song.mp3"
    output_name = "song.wav"
    with open("song.mp3", "wb") as f:
        f.write(data)
    os.system(f"ffmpeg -i {file_name} {output_name}")

    with open(output_name, "rb") as f:
        transcription = transcript_data(f)

    response = requests.post(
        f"{BASE_URL}/answer/{token}", json={"answer": transcription}
    ).json()

    print(response)


if __name__ == "__main__":
    main("whisper")
