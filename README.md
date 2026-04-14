# Penguin Jokes

AI-powered dad jokes. Fetch a random joke, have GPT explain it, hear it read aloud, or see an AI-generated illustration.

Live at [penguinjokes.lol](https://penguinjokes.lol)

## Features

- **Laugh** — fetch a random dad joke from [icanhazdadjoke.com](https://icanhazdadjoke.com/)
- **Explain** — GPT-4o-mini breaks down why the joke is funny
- **Read** — OpenAI TTS reads the joke aloud with a random voice
- **Draw** — DALL-E 3 generates an illustration of the joke

Explanations and images are cached in SQLite so repeat requests are instant.

## Setup

```bash
uv sync
cp .env.example .env  # add your OPENAI_API_KEY
uv run python app.py
```

## Stack

- Flask + Jinja2
- OpenAI API (GPT-4o-mini, TTS-1, DALL-E 3)
- SQLite via SQLModel
- Tailwind CSS
