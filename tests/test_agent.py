from ducky.agent.agent import Agent
from ducky.models.openrouter_model import OpenRouterModel

def test_query():
    model = OpenRouterModel(model_name="nvidia/nemotron-3-super-120b-a12b:free")
    agent = Agent(model)
    agent.n_calls = 0

    agent.add_messages({
        "role": "user",
        "content": "Hello, Whats the capital of India?!"
        })

    result = agent.query()
    assert isinstance(result, dict)
    assert result["role"] == "assistant"
    assert result["content"]
    assert agent.n_calls == 1

    print(result["content"])

