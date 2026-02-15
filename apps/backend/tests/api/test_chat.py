"""
Tests for chat endpoints.
"""


def test_chat_completions_invalid_model(client):
    """Sending an invalid model name should return 422."""
    response = client.post(
        "/api/v1/chat/completions",
        json={"message": "Hello", "model": "invalid-model"},
    )
    assert response.status_code == 422


def test_chat_completions_empty_message(client):
    """Sending an empty message should return 422."""
    response = client.post(
        "/api/v1/chat/completions",
        json={"message": "", "model": "gpt-4"},
    )
    assert response.status_code == 422
