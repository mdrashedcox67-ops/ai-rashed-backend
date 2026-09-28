from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def generate_chat_response(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> str:
        pass
