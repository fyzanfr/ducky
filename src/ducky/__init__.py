from dataclasses import dataclass 
from typing import Any, Mapping, Protocol

class Model(Protocol):
    def query(
            self,
            messages: list[dict[str, Any]],
            **kwargs: Any,
            ) -> dict[str, Any]: ...


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


    def get_info(self) -> dict[str, Any]: ...
