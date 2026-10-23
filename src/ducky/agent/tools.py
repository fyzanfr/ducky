EXECUTE_TOOL = {
    "type": "function",
    "function": {
        "name": "execute",
        "description": (
            "Execute a command and return stdout, stderr, and exit code. "
            "Commands are non-interactive."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "anyOf": [
                        {"type": "string"},
                        {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    ],
                    "description": "The command to execute.",
                },
                "cwd": {
                    "type": "string",
                    "description": "Working directory for the command.",
                },
                "timeout": {
                    "type": "number",
                    "description": "Maximum execution time in seconds.",
                },
                "env": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Additional environment variables.",
                },
            },
            "required": ["command"],
            "additionalProperties": False,
        },
    },
}

SEND_MESSAGE_TOOL = {
    "type": "function",
    "function": {
        "name": "send_message",
        "description": ("Send a message to the user."),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": ("Content of the message"),
                },
            },
            "required": ["summary"],
            "additionalProperties": False,
        },
    },
}

