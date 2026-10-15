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


''' class Agent:
    def __init__(self, model: Model):






    def step(self) -> list[dict]:
        """ Query the LM, execute the actions"""
        return self.execute_actions(self.query())



    def execute_actions(self, messages: dict) -> list[dict]:
        """Execute actions in message, add observation messages, return them."""

'''


### Prototype provided by the mini-swe-agent at minimal-agent.com 

# things required to implement
def query_lm(messages: list[dict[str, str]]) -> str:
    response = completion(
            model = "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
            messages = messages
        )
    return response.choices[0].message.content 

 
def parse_action(lm_output: str) -> str:
    "Take LM output, return action"
    matches = re.findall(
            r"```bash-action\s*\n(.*?)\n```",
            lm_output,
            re.DOTALL
        )
    return matches[0].strip() if matches else ""

def execute_actions(command: str) -> str:
    """ Execute action, return output"""
    result = subprocess.run(
            command, 
            shell=True,
            text=True,
            env=os.environ,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
    return result.stdout

messages = [{
    "role": "system", 
    "content": "You are a helpful assistant. When you want to run a command, wrap it in ```bash-action\n<command>\n```. To finish, run the exit command."
    }, {
        "role": "user", 
        "content": "Write some info about attention mechanism in tests_by_agent directory in a file name Attention-mech-info.txt."
        }]

'''while True:
    lm_output = query_lm(messages)
    print("LM output", lm_output)
    messages.append({"role": "assistant", "content": lm_output}) # remembering what LM said
    action = parse_action(lm_output) # separate the action from output 
    print("Action", action)
    if action == "exit":
        break
    output = execute_actions(action)
    print("Output", output)
    messages.append({"role": "user", "content": output})   # sending command output back
'''

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
        self.messages: list[dict] = []

    #def run(self, task: str = "") -> dict:


    def add_messages(self, *messages: dict) -> str:
        self.messages.extend(messages)
        return list(messages)

    #def step(self) -> list[dict]:
    #    """ Query the LM, Execute the Action """
    #    return self.execute_actions(self.query())

    def query(self) -> dict:
        """ Query the model and return model messages. Override to add hooks."""
        self.n_calls += 1
        messages = self.model.query(self.messages)
        self.add_messages(*messages)
        return messages

