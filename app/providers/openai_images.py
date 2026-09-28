from __future__ import annotations

from openai import OpenAI


class OpenAIImageProvider:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_image(self, prompt: str, model: str | None = None) -> str:
        selected_model = model or "dall-e-3"
        response = self.client.images.generate(
            model=selected_model,
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        return response.data[0].url or ""

    def edit_image(
        self,
        prompt: str,
        image_bytes: bytes,
        mask_bytes: bytes | None = None,
        model: str | None = None,
    ) -> str:
        selected_model = model or "dall-e-2"
        
        kwargs = {
            "model": selected_model,
            "image": image_bytes,
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
        }
        if mask_bytes:
            kwargs["mask"] = mask_bytes

        response = self.client.images.edit(**kwargs)
        return response.data[0].url or ""
