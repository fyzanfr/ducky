import os
import requests

class OpenRouterModel:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.api_key = os.environ["OPENROUTER_API_KEY"]
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def query(self, messages: list[dict]) -> list[dict]:
        response = requests.post(
                self.url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model_name,
                    "messages": messages,
                    },
                timeout=60,
                )

        if not response.ok:
            raise RuntimeError(
                f"OpenRouter API error ({response.status_code}): "
                f"{response.text}"
        )

        data = response.json()
        return data["choices"][0]["message"]
