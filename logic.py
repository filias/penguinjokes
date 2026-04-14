import random
import re
import uuid
from pathlib import Path

import requests
from openai import OpenAI

from models import get_joke_by_id, save_joke, update_joke_explanation, update_joke_image

JOKES_API_URL = "https://icanhazdadjoke.com/"
VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
_openai_client = None


def _get_openai():
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI()
    return _openai_client


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

    response = _get_openai().chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Explain the joke: {joke}"},
        ],
    )
    explanation = response.choices[0].message.content.strip()

    if joke_id:
        update_joke_explanation(joke_id, explanation)

    return explanation


def read_joke(joke: str, voice: str = "random") -> str:
    if voice == "random" or voice not in VOICES:
        voice = random.choice(VOICES)
    response = _get_openai().audio.speech.create(model="tts-1", voice=voice, input=joke)

    filename = f"{uuid.uuid4().hex}.mp3"
    audio_path = Path("static/audio") / filename
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    with open(audio_path, "wb") as audio_file:
        audio_file.write(response.content)

    return str(audio_path)


def draw_joke(joke: str, joke_id: str = None) -> str:
    if joke_id:
        db_joke = get_joke_by_id(joke_id=joke_id)
        if db_joke and db_joke.image:
            return db_joke.image

    response = _get_openai().images.generate(
        model="dall-e-3", prompt=joke, size="1024x1024", quality="standard", n=1
    )

    # Download and save locally so the URL doesn't expire
    image_data = requests.get(response.data[0].url).content
    filename = f"{uuid.uuid4().hex}.png"
    image_path = Path("static/images") / filename
    image_path.parent.mkdir(parents=True, exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(image_data)

    local_url = f"/static/images/{filename}"
    if joke_id:
        update_joke_image(joke_id, local_url)

    return local_url
