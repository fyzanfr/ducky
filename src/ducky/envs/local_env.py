import os
import subprocess
from pathlib import Path
from typing import Mapping
import platform

from ducky import ExecResult, Env

class LocalEnvironment:
    """Execute shell commands on the local machine."""

    def __init__(self, cwd: str | Path | None = None):
        self.cwd = Path(cwd or Path.cwd()).expanduser().resolve()

        if not self.cwd.is_dir():
            raise NotADirectoryError(
                f"Working directory does not exist: {self.cwd}"
            )

    def execute(
        self,
        command: str | list[str],
        *,
        cwd: str | None = None,
        timeout: float = 30.0,
        env: Mapping[str, str] | None = None,
    ) -> ExecResult:
        """Execute a command and capture its result."""

        if isinstance(command, str):
            if not command.strip():
                raise ValueError("Command cannot be empty")
            shell = True

        elif isinstance(command, list) and command and all(
            isinstance(arg, str) for arg in command
        ):
            shell = False

        else:
            raise ValueError(
                "Command must be a non-empty string or list of strings"
            )

        if timeout <= 0:
            raise ValueError("Timeout must be positive")

        workdir = Path(cwd).expanduser().resolve() if cwd else self.cwd

        if not workdir.is_dir():
            return ExecResult(
                stdout="",
                stderr=f"Working directory does not exist: {workdir}",
                exit_code=2,
                time_out=False,
            )

        process_env = os.environ.copy()
        if env:
            process_env.update(env)

        try:
            result = subprocess.run(
                command,
                shell=shell,
                cwd=workdir,
                env=process_env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            return ExecResult(
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                time_out=False,
            )

        except subprocess.TimeoutExpired as exc:
            def as_text(value):
                if value is None:
                    return ""
                if isinstance(value, bytes):
                    return value.decode(errors="replace")
                return value

            return ExecResult(
                stdout=as_text(exc.stdout),
                stderr=as_text(exc.stderr),
                exit_code=None,
                time_out=True,
            )

    def close(self) -> None:
        """No persistent resources to release."""
        pass


    def get_info(self) -> dict[str, str]:
        info = platform.uname()

        return {
                "system": info.system,
                "release": info.release,
                "version": info.version,
                "machine": info.machine,
                "working_directory": str(self.cwd),
            }
