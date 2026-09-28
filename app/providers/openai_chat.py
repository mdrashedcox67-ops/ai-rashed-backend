from __future__ import annotations

from typing import Any
from openai import OpenAI
from app.providers.base import BaseProvider


class OpenAIChatProvider(BaseProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = OpenAI(api_key=self.api_key)

    def generate_chat_response(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> str:
        selected_model = model or "gpt-4o"
        
        # Build prompt payload
        formatted_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted_messages.append({"role": role, "content": content})

        response = self.client.chat.completions.create(
            model=selected_model,
            messages=formatted_messages,
        )

        return response.choices[0].message.content or ""
