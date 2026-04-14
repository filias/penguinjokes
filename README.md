# Penguin Jokes

AI-powered dad jokes. Fetch a random joke, have GPT explain it, hear it read aloud, or see an AI-generated illustration.

Live at [penguinjokes.lol](https://penguinjokes.lol)

## Setup

```bash
uv sync
cp .env.example .env  # add your OPENAI_API_KEY
uv run python app.py
```

## How it works

- Jokes come from [icanhazdadjoke.com](https://icanhazdadjoke.com/)
- **Explain** uses GPT-4o
- **Read** uses OpenAI TTS
- **Draw** uses DALL-E 3
