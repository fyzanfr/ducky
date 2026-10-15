from typing import Any, Protocol

class Model(Protocol):
    """ Interface that model must satisfy. """

    def query(self, messages: list[dict[Any, Any]]) -> dict[str, Any]: ...

