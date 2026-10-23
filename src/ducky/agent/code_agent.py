from __future__ import annotations

import json
from typing import Any

from ducky import Environment, Model
from ducky.agent.agent import Agent
from ducky.agent.tools import EXECUTE_TOOL, SEND_MESSAGE_TOOL
from ducky.envs.local_env import LocalEnvironment

class CodeAgent(Agent):
    """Coding agent with command execution and final responses."""

    def __init__(
            self,
            model: Model,
            env: Environment,
            task: str,
            step_limit: int = 100,
            ):

        super().__init__(model, env, step_limit)

        self.task = task
        self.final_answer = ""

        self.tools.extend([EXECUTE_TOOL, SEND_MESSAGE_TOOL])

        sys_info = json.dumps(self.env.get_info(), indent=2)

        self.system_prompt = f"""
        You are an expert coding agent.
        Inspect the codebase, implement the requested changes,
        and run relevant tests to verify your work.

        <system_information>
        {sys_info}
        </system_information>

        Use the execute tool to run commands.
        Use send_message when the task is complete.
        """

        self.task_prompt = self.task 


    def execute_tool_calls(
            self, 
            tool_calls: list[dict[str, Any]]
            ) -> list[dict[str, str]]:
        """Execute tool calls and return observations."""
        observations = []
        for tool_call in tool_calls:
            call_id = tool_call.get("id", "")
            function = tool_call.get("function", {})
            tool_name = function.get("name", "unknown")

            try:
                raw_arguments = function.get("arguments", "{}")
                arguments = (
                        json.loads(raw_arguments)
                        if isinstance(raw_arguments, str)
                        else raw_arguments
                    )

                if not isinstance(arguments, dict):
                    raise ValueError("Arguments must be a JSON object")

            except (json.JSONDecodeError, TypeError, ValueError) as exc:
                content = f"Invalid tool arguments: {exc}"


            else: 
                if tool_name == "execute":
                    try:
                        result = self.env.execute(**arguments)
                        content = json.dumps({
                            "stdout": result.stdout,
                            "stderr": result.stderr,
                            "exit_code": result.exit_code,
                            "timed_out": result.timed_out,
                        })
                    except Exception as exc:
                        content = f"Tool execution failed: {exc}"

                elif tool_name == "send_message":
                    message = arguments.get("message")

                    if not isinstance(message, str):
                        content = (
                            "Invalid send_message arguments: "
                            "message must be a string"
                        )
                    else:
                        self.final_answer = message
                        self.finished = True
                        content = "Final message received."

                else:
                    content = f"Unknown tool: {tool_name}"

            observations.append({
                "role": "tool",
                "tool_call_id": call_id,
                "content": content,
            })

        return observations

