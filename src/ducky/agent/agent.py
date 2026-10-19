import json
import logging
import time
import traceback
from pathlib import Path 
from pydantic import BaseModel
import os 
import subprocess
from litellm import completion
import re
from typing import Any
from ducky import Model


class Agent:
    """ Agent Class, consists of following functions:
            def fun: 
            def step:
            def query:
            def execute_actions:

        """
    def __init__(self, model: Model):
        self.model = model
        #self.env = env
        self.msgs: list[dict] = []
        self.finished: bool = False
        self.tools
        self.step_limit: int = 100
        self.system_prompt: str = ""
        self.task_prompt:str = ""

    #def run(self, task: str = "") -> dict:


    def build_prompt(self) -> list[dict[str, Any]]:
        prompt = [{"role": "system", "content": self.system_prompt},
                  {"role": "user", "content": self.task_prompt}]

        prompt.extend(self.messages)
        return prompt
    #def step(self) -> list[dict]:
    #    """ Query the LM, Execute the Action """
    #    return self.execute_actions(self.query())

    def execute_actions(self, messages:dict) -> list[dict]:
        """Execute actions in message, return them."""
        outputs = 

    def query(self) -> dict:
        """ Query the model and return model messages. Override to add hooks."""
        self.n_calls += 1
        messages = self.model.query(self.messages)
        self.add_messages(*messages)
        return messages

