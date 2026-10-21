
import sys

import pytest

from ducky.envs.local_env import LocalEnvironment


@pytest.fixture
def env(tmp_path):
    """Create a local environment with a temporary working directory."""
    return LocalEnvironment(cwd=tmp_path)


def test_execute_string_command(env):
    """A shell command should execute and return its output."""
    result = env.execute("printf 'hello'")

    assert result.stdout == "hello"
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.time_out is False


def test_execute_list_command(env):
    """A list command should execute directly, without shell parsing."""
    result = env.execute(
        [sys.executable, "-c", "print('hello')"]
    )

    assert result.stdout == "hello\n"
    assert result.exit_code == 0
    assert result.time_out is False


def test_list_command_does_not_interpret_shell_syntax(env):
    """Shell metacharacters should remain ordinary arguments in list form."""
    result = env.execute([
        sys.executable,
        "-c",
        "import sys; print(sys.argv[1])",
        "hello; echo unexpected",
    ])

    assert result.stdout == "hello; echo unexpected\n"
    assert result.exit_code == 0


def test_command_failure_returns_exit_code(env):
    """A nonzero command exit should be returned, not raised."""
    result = env.execute(
        [sys.executable, "-c", "raise SystemExit(7)"]
    )

    assert result.exit_code == 7
    assert result.time_out is False


def test_command_timeout(env):
    """A timed-out process should be reported clearly."""
    result = env.execute(
        [sys.executable, "-c", "import time; time.sleep(2)"],
        timeout=0.2,
    )

    assert result.time_out is True
    assert result.exit_code is None


@pytest.mark.parametrize(
    "command",
    [
        "",
        "   ",
        [],
        ["echo", 123],
        123,
        None,
    ],
)
def test_invalid_command_is_rejected(env, command):
    """Invalid command input should fail before subprocess execution."""
    with pytest.raises((ValueError, TypeError)):
        env.execute(command)


@pytest.mark.parametrize("timeout", [0, -1, -0.5])
def test_nonpositive_timeout_is_rejected(env, timeout):
    with pytest.raises(ValueError, match="Timeout"):
        env.execute("echo hello", timeout=timeout)


def test_missing_working_directory_returns_error(env, tmp_path):
    """A nonexistent per-command directory should not run the command."""
    missing_dir = tmp_path / "does-not-exist"

    result = env.execute("echo hello", cwd=str(missing_dir))

    assert result.stdout == ""
    assert "Working directory does not exist" in result.stderr
    assert result.exit_code == 2
    assert result.time_out is False


def test_constructor_rejects_invalid_working_directory(tmp_path):
    """The default directory must exist."""
    missing_dir = tmp_path / "does-not-exist"

    with pytest.raises(NotADirectoryError):
        LocalEnvironment(cwd=missing_dir)


def test_relative_execution_uses_environment_working_directory(tmp_path):
    """Commands should run from the configured default directory."""
    env = LocalEnvironment(cwd=tmp_path)

    result = env.execute(["pwd"])

    assert result.exit_code == 0
    assert result.stdout.strip() == str(tmp_path.resolve())


def test_per_command_environment_overrides_and_inherits(env, monkeypatch):
    """Custom variables should be added without losing inherited variables."""
    monkeypatch.setenv("DUCKY_INHERITED_TEST", "inherited")

    result = env.execute(
        [
            sys.executable,
            "-c",
            (
                "import os; "
                "print(os.environ['DUCKY_CUSTOM_TEST']); "
                "print(os.environ['DUCKY_INHERITED_TEST'])"
            ),
        ],
        env={"DUCKY_CUSTOM_TEST": "custom"},
    )

    assert result.exit_code == 0
    assert result.stdout == "custom\ninherited\n"


def test_close_is_safe_to_call(env):
    """Closing a local environment should not raise."""
    env.close()
    env.close()

