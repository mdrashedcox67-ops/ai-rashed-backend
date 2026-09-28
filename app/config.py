from __future__ import annotations

import os


class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    APP_TOKENS: list[str] = [
        token.strip()
        for token in os.getenv("APP_TOKENS", "").split(",")
        if token.strip()
    ]
