from dataclasses import dataclass 
from typing import Mapping, Protocol

@dataclass
class ExecResult:
    stdout: str
    stderr: str 
    exit_code: int | None
    time_out: bool


class Env(Protocol):
    """ Execute the shell commands locally or in a persistent, local Docker container."""

    def execute(
            self,
            command: str,
            *,
            cwd: str | None = None,
            timeout: float = 30.0,
            env: Mapping[str, str] | None = None, 
            ) -> ExecResult:
        """Execute a command and return its result."""
        ...

    def close(self) -> None:
        """Release resources owned by this environment."""
        ...

