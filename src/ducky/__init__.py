from typing import Any, Protocol

class Model(Protocol):
    def query(
            self,
            messages: list[dict[str, Any]],
            **kwargs: Any,
            ) -> dict[str, Any]: ...

