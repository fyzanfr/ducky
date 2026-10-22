from unittest.mock import Mock

import pytest
import requests

from ducky.models import openrouter_model
from ducky.models.openrouter_model import OpenRouterModel


def test_query_sends_request_and_returns_message(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    message = {"role": "assistant", "content": "Hello!"}

    response = Mock()
    response.json.return_value = {
        "choices": [{"message": message}]
    }

    post = Mock(return_value=response)
    monkeypatch.setattr(openrouter_model.requests, "post", post)

    model = OpenRouterModel()
    messages = [{"role": "user", "content": "Hi"}]
    tools = []

    result = model.query(
        messages,
        tools=tools,
        max_completion_tokens=100,
    )

    assert result == message

    post.assert_called_once_with(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": "Bearer test-key"},
        json={
            "model": "openai/gpt-4o-mini",
            "messages": messages,
            "tools": tools,
            "max_completion_tokens": 100,
        },
        timeout=60,
    )


def test_query_raises_on_http_error(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError(
        "Request failed"
    )

    monkeypatch.setattr(
        openrouter_model.requests,
        "post",
        Mock(return_value=response),
    )

    model = OpenRouterModel()

    with pytest.raises(requests.HTTPError):
        model.query([{"role": "user", "content": "Hi"}])
