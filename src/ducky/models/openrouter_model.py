import os
from typing import Any

import requests


class OpenRouterModel:
    def __init__(self):
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        self.api_key = os.environ["OPENROUTER_API_KEY"]

    def query(
        self,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": messages, **kwargs},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]
