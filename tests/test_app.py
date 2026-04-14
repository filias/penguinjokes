"""Tests for Flask routes."""

from unittest.mock import patch

import pytest

from app import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch(
    "app.get_joke",
    return_value=("id-1", "Why did the chicken cross the road?", " Other side."),
)
def test_index_returns_joke(mock_get, client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"chicken" in response.data


@patch(
    "app.get_joke",
    return_value=("id-2", "What do you call a fake noodle?", " An impasta."),
)
def test_laugh_returns_json(mock_get, client):
    response = client.get("/laugh")
    assert response.status_code == 200
    data = response.get_json()
    assert "joke" in data
    assert "impasta" in data["joke"]


@patch("app.explain_joke", return_value="It's a pun on impostor and pasta.")
def test_explain_returns_text(mock_explain, client):
    response = client.get("/explain?joke=What+do+you+call+a+fake+noodle&joke_id=id-1")
    assert response.status_code == 200
    data = response.get_json()
    assert "text" in data
    assert "pun" in data["text"]


@patch("app.read_joke", return_value="static/audio/test.mp3")
def test_read_returns_audio_path(mock_read, client):
    response = client.get("/read?joke=test+joke&voice=nova")
    assert response.status_code == 200
    data = response.get_json()
    assert "audio_path" in data
    mock_read.assert_called_once_with("test joke", voice="nova")


@patch("app.draw_joke", return_value="/static/images/test.png")
def test_draw_returns_image_url(mock_draw, client):
    response = client.get("/draw?joke=test+joke&joke_id=id-1")
    assert response.status_code == 200
    data = response.get_json()
    assert "image_url" in data


def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"Penguin Jokes" in response.data
    assert b"memi" in response.data
