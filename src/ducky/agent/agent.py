import json
import logging
import time
import traceback
from pathlib import Path 
from pydantic import BaseModel
import os 
import subprocess
import re
from typing import Any
from ducky import Model



class StepLimitError(Exception):
    """Raised when an agent exhausts its model-call budget."""


class Agent:
    """ Base class for a ReAct agent with pluggale tools. """
    def __init__(self, 
                 model: Model,
                 env: Environment,
                 step_limit: int = 100,
                 ):
        self.model = model
        self.env = env
        self.msgs: list[dict] = []
        self.finished: bool = False
        self.tools: list[dict[str, Any]] = []
        self.step_limit = step_limit
        self.system_prompt: str = ""
        self.task_prompt:str = ""
        self.steps_taken = 0

    def build_prompt(self) -> list[dict[str, Any]]:
        prompt = [{"role": "system", "content": self.system_prompt},
                  {"role": "user", "content": self.task_prompt}]
        # include prior conv history
        prompt.extend(self.msgs)
        return prompt

    
    def execute_tool(
            self, tool_calls:list[dict[str, Any]]
            ) -> list[dict]: 
        """Execute domain-specific tool_calls and return thier observations.""" 
        # not implemented cause its domain-specific
        raise NotImplementedError


    def query(self) -> dict:
        """ Send one tool-enabled Chat Completion request """
        
        messages = self.build_prompt()
        #self.api_prompts.append(deepcopy(messages))
        step_number = self.steps_taken + 1
        print(
            f"[agent] step {step_number}/{self.step_limit}: requesting action",
            flush=True,
        )
        try:
            response = self.model.query(
                    messages,
                    tools=self.tools,
                    reasoning_effort="medium",
                    max_completion_tokens=4096,
            )
        except Exception as exc:
            print(
                f"[agent] step {step_number}: model request failed after retries "
                f"({type(exc).__name__}: {exc})",
                flush=True,
            )
            raise
        #self.api_responses.append(response.model_dump(mode="json"))
        self.steps_taken += 1
        message = response
        tool_names = [
            call.get("function", {}).get("name", "unknown")
            for call in message.get("tool_calls", [])
            if isinstance(call, dict)
        ]
        if tool_names:
            print(
                f"[agent] step {step_number}: tool call(s): {', '.join(tool_names)}",
                flush=True,
            )
        else:
            print(
                f"[agent] step {step_number}: response contained no parsed tool call; "
                "the loop should preserve the response and continue",
                flush=True,
            )
        return message


    def run(self) -> None:
        """ Run ReAct steps, save trajetory."""
        try:
            while not self.finished:
                if self.steps_taken >= self.step_limit:
                    raise StepLimitError("Agent exceeded the step limits")
                #self.maybe_compact_context()
                message = self.query()
                self.msgs.append(message)
                tool_calls = message.get("tool_calls", [])

                if tool_calls:
                    tool_results = self.execute_tool(tool_calls)
                    self.msgs.extend(tool_results)

        finally:
            self.env.close()





