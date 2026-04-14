import os
from urllib.parse import unquote

from flask import Flask, render_template, request
from dotenv import load_dotenv

from logic import explain_joke, get_joke, read_joke, draw_joke

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    joke_id, question, answer = get_joke()
    return render_template(
        "index.html",
        joke=f"{question} {answer}",
        question=question,
        answer=answer,
        joke_id=joke_id,
    )


@app.route("/laugh")
def laugh():
    joke_id, question, answer = get_joke()
    return {"joke": f"{question} {answer}"}, 200


@app.route("/explain")
def explain():
    joke = unquote(request.args.get("joke", ""))
    joke_id = request.args.get("joke_id")
    explanation = explain_joke(joke, joke_id=joke_id)
    return {"text": explanation}, 200


@app.route("/read")
def read():
    joke = unquote(request.args.get("joke", ""))
    audio_path = read_joke(joke)
    return {"audio_path": str(audio_path)}, 200


@app.route("/draw")
def draw():
    joke = unquote(request.args.get("joke", ""))
    joke_id = request.args.get("joke_id")
    image_url = draw_joke(joke, joke_id=joke_id)
    return {"image_url": str(image_url)}, 200


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
