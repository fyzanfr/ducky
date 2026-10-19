from dataclasses import dataclass, field
from typing import Any, Literal, Protocol, Sequence

Role = Literal["system", "user", "assistant", "tool"]

@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]

@dataclass
class Message:
    role: Role
    content: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_call_id: str | None = None

@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema

@dataclass(frozen=True)
class ModelRequest:
    messages: Sequence[Message]
    tools: Sequence[ToolDefinition] = ()
    temperature: float | None = None
    max_output_tokens: int | None = None

@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

@dataclass(frozen=True)
class ModelResponse:
    message: Message
    model: str | None = None
    finish_reason: str | None = None
    usage: TokenUsage | None = None

class Model(Protocol):
    @property
    def supports_tools(self) -> bool:
        ...

    def complete(self, request: ModelRequest) -> ModelResponse:
        ...

