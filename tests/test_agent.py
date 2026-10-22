import pytest

from ducky.agent.agent import Agent


class FakeModel:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.messages = None
        self.kwargs = None

    def query(self, messages, **kwargs):
        self.messages = messages
        self.kwargs = kwargs

        if self.error:
            raise self.error

        return self.response


class FakeEnv:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


def test_build_prompt():
    agent = Agent(FakeModel(), FakeEnv())
    agent.system_prompt = "You are a coding agent"
    agent.task_prompt = "Fix the bug"
    agent.msgs.append(
        {"role": "assistant", "content": "Previous response"}
    )

    prompt = agent.build_prompt()

    assert prompt == [
        {"role": "system", "content": "You are a coding agent"},
        {"role": "user", "content": "Fix the bug"},
        {"role": "assistant", "content": "Previous response"},
    ]


def test_query_calls_model_and_returns_response():
    response = {"role": "assistant", "content": "Done"}
    model = FakeModel(response=response)
    agent = Agent(model, FakeEnv())
    agent.system_prompt = "System"
    agent.task_prompt = "Do task"
    agent.tools = [{"type": "function", "function": {"name": "test"}}]

    result = agent.query()

    assert result == response
    assert model.messages == [
        {"role": "system", "content": "System"},
        {"role": "user", "content": "Do task"},
    ]
    assert model.kwargs["tools"] == agent.tools
    assert model.kwargs["reasoning_effort"] == "medium"
    assert model.kwargs["max_completion_tokens"] == 4096
    assert agent.steps_taken == 1


def test_query_propagates_model_error():
    model = FakeModel(error=RuntimeError("API unavailable"))
    agent = Agent(model, FakeEnv())

    with pytest.raises(RuntimeError, match="API unavailable"):
        agent.query()

    assert agent.steps_taken == 0


def test_run_executes_tool_and_closes_environment():
    tool_call = {
        "id": "call_1",
        "type": "function",
        "function": {
            "name": "test_tool",
            "arguments": "{}",
        },
    }
    response = {
        "role": "assistant",
        "content": None,
        "tool_calls": [tool_call],
    }
    tool_result = {
        "role": "tool",
        "tool_call_id": "call_1",
        "content": "Success",
    }

    class ToolAgent(Agent):
        def execute_tool(self, tool_calls):
            assert tool_calls == [tool_call]
            self.finished = True
            return [tool_result]

    env = FakeEnv()
    agent = ToolAgent(FakeModel(response=response), env)

    agent.run()

    assert agent.msgs == [response, tool_result]
    assert agent.finished is True
    assert env.closed is True
