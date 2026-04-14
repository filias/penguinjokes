"""Tests for business logic — OpenAI calls are mocked."""

from unittest.mock import MagicMock, patch

from logic import VOICES, explain_joke, get_joke, read_joke


@patch("logic.save_joke", return_value="joke-id-1")
@patch("logic.requests.get")
def test_get_joke_with_question(mock_get, mock_save):
    mock_get.return_value.json.return_value = {
        "joke": "Why did the chicken cross the road? To get to the other side."
    }
    joke_id, question, answer = get_joke()
    assert joke_id == "joke-id-1"
    assert "chicken" in question
    assert "?" in question
    assert "other side" in answer


@patch("logic.save_joke", return_value="joke-id-2")
@patch("logic.requests.get")
def test_get_joke_without_question(mock_get, mock_save):
    mock_get.return_value.json.return_value = {
        "joke": "I used to hate facial hair but then it grew on me."
    }
    joke_id, question, answer = get_joke()
    assert "facial hair" in question
    assert answer == ""


@patch("logic.get_joke_by_id")
def test_explain_joke_returns_cached(mock_get_by_id):
    mock_joke = MagicMock()
    mock_joke.explanation = "It's a pun."
    mock_get_by_id.return_value = mock_joke

    result = explain_joke("some joke", joke_id="id-1")
    assert result == "It's a pun."


@patch("logic.update_joke_explanation")
@patch("logic._get_openai")
@patch(
    "logic.get_joke_by_id",
    return_value=MagicMock(explanation=None),
)
def test_explain_joke_calls_openai(mock_get_by_id, mock_openai, mock_update):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "  It's funny because...  "
    mock_openai.return_value.chat.completions.create.return_value = mock_response

    result = explain_joke("Why?", joke_id="id-1")
    assert result == "It's funny because..."
    mock_update.assert_called_once_with("id-1", "It's funny because...")


def test_read_joke_with_specific_voice():
    with patch("logic._get_openai") as mock_openai:
        mock_response = MagicMock()
        mock_response.content = b"fake-audio"
        mock_openai.return_value.audio.speech.create.return_value = mock_response

        result = read_joke("test joke", voice="nova")
        assert result.endswith(".mp3")
        mock_openai.return_value.audio.speech.create.assert_called_once_with(
            model="tts-1", voice="nova", input="test joke"
        )


def test_read_joke_random_voice():
    with patch("logic._get_openai") as mock_openai:
        mock_response = MagicMock()
        mock_response.content = b"fake-audio"
        mock_openai.return_value.audio.speech.create.return_value = mock_response

        read_joke("test joke", voice="random")
        call_args = mock_openai.return_value.audio.speech.create.call_args
        assert call_args.kwargs["voice"] in VOICES


def test_read_joke_invalid_voice_falls_back_to_random():
    with patch("logic._get_openai") as mock_openai:
        mock_response = MagicMock()
        mock_response.content = b"fake-audio"
        mock_openai.return_value.audio.speech.create.return_value = mock_response

        read_joke("test joke", voice="invalid_voice")
        call_args = mock_openai.return_value.audio.speech.create.call_args
        assert call_args.kwargs["voice"] in VOICES
