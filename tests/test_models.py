"""Tests for database models."""

import pytest
from sqlmodel import SQLModel

from models import (
    engine,
    get_joke_by_id,
    save_joke,
    update_joke_explanation,
    update_joke_image,
)


@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    """Use a temporary database for each test."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr("models.sqlite_filename", str(db_path))
    monkeypatch.setattr("models.engine", engine)
    SQLModel.metadata.create_all(engine)
    yield


def test_save_and_retrieve_joke():
    joke_id = save_joke(
        "Why did the chicken cross the road?", "To get to the other side."
    )
    assert joke_id is not None

    joke = get_joke_by_id(joke_id)
    assert joke.question == "Why did the chicken cross the road?"
    assert joke.answer == "To get to the other side."


def test_save_duplicate_returns_same_id():
    id1 = save_joke("Duplicate joke?", "Same answer.")
    id2 = save_joke("Duplicate joke?", "Same answer.")
    assert id1 == id2


def test_update_joke_explanation():
    joke_id = save_joke("Test joke?", "Answer.")
    update_joke_explanation(joke_id, "It's a test.")

    joke = get_joke_by_id(joke_id)
    assert joke.explanation == "It's a test."


def test_update_joke_image():
    joke_id = save_joke("Image joke?", "Answer.")
    update_joke_image(joke_id, "/static/images/test.png")

    joke = get_joke_by_id(joke_id)
    assert joke.image == "/static/images/test.png"
