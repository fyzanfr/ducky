from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider


model = OllamaModel(
    'qwen2.5-coder:3b', provider=OllamaProvider(base_url='http://localhost:11434/v1')
)
agent = Agent(model)

result = agent.run_sync("What is the capital of France?")

print(result.output)
