import random
import re
import uuid
from pathlib import Path

from openai import OpenAI
import requests

from models import save_joke, get_joke_by_id

JOKES_API_URL = "https://icanhazdadjoke.com/"
VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
openai_client = OpenAI()


def get_joke() -> tuple[str, str, str]:
    response = requests.get(JOKES_API_URL, headers={"Accept": "application/json"})
    joke = response.json()["joke"]

    if "?" not in joke:
        question = joke
        answer = ""
    else:
        question, answer = re.split(r"(?<=\?)", joke)
        answer = answer.strip()

    joke_id = save_joke(question, answer)
    return joke_id, question, answer


def explain_joke(joke: str, joke_id: str = None) -> str:
    if joke_id:
        db_joke = get_joke_by_id(joke_id=joke_id)
        if db_joke and db_joke.explanation:
            return db_joke.explanation

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Explain the joke: {joke}"},
        ],
    )
    return response.choices[0].message.content.strip()


def read_joke(joke: str) -> str:
    voice = random.choice(VOICES)
    response = openai_client.audio.speech.create(model="tts-1", voice=voice, input=joke)

    filename = f"{uuid.uuid4().hex}.mp3"
    audio_path = Path("static/audio") / filename
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    with open(audio_path, "wb") as audio_file:
        audio_file.write(response.content)

    return str(audio_path)


def draw_joke(joke: str, joke_id: str = None) -> str:
    response = openai_client.images.generate(
        model="dall-e-3", prompt=joke, size="1024x1024", quality="standard", n=1
    )
    return response.data[0].url
