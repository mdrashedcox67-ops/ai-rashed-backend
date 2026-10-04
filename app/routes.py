from __future__ import annotations

import base64
from flask import Blueprint, current_app, jsonify, request, render_template
from app.errors import make_error_response
from app.providers.openai_chat import OpenAIChatProvider
from app.providers.openai_images import OpenAIImageProvider
from app.security import require_app_token

bp = Blueprint("routes", __name__)


@bp.get("/")
def home():
    return render_template('index.html')


@bp.get("/health")
def health_check():
    return jsonify({"status": "ok", "service": "ai-rashed-backend"}), 200


@bp.post("/v1/chat")
@require_app_token
def handle_chat():
    data = request.get_json() or {}
    messages = data.get("messages", [])
    model = data.get("model")
    attachments = data.get("attachments", [])

    if not messages:
        return make_error_response("messages are required", 400)

    api_key = current_app.config.get("OPENAI_API_KEY")
    if not api_key:
        return make_error_response("Server misconfiguration: OPENAI_API_KEY is missing", 500)

    provider = OpenAIChatProvider(api_key=api_key)
    try:
        response_text = provider.generate_chat_response(
            messages=messages,
            model=model,
            attachments=attachments,
        )
        return jsonify({"response": response_text}), 200
    except Exception as e:
        return make_error_response(str(e), 500)


@bp.post("/v1/images/generate")
@require_app_token
def handle_image_generate():
    data = request.get_json() or {}
    prompt = data.get("prompt")
    model = data.get("model")

    if not prompt:
        return make_error_response("prompt is required", 400)

    api_key = current_app.config.get("OPENAI_API_KEY")
    if not api_key:
        return make_error_response("Server misconfiguration: OPENAI_API_KEY is missing", 500)

    provider = OpenAIImageProvider(api_key=api_key)
    try:
        image_url = provider.generate_image(prompt=prompt, model=model)
        return jsonify({"image_url": image_url}), 200
    except Exception as e:
        return make_error_response(str(e), 500)


@bp.post("/v1/images/edit")
@require_app_token
def handle_image_edit():
    data = request.get_json() or {}
    prompt = data.get("prompt")
    image_b64 = data.get("image")
    mask_b64 = data.get("mask")
    model = data.get("model")

    if not prompt or not image_b64:
        return make_error_response("prompt and image are required", 400)

    api_key = current_app.config.get("OPENAI_API_KEY")
    if not api_key:
        return make_error_response("Server misconfiguration: OPENAI_API_KEY is missing", 500)

    try:
        image_bytes = base64.b64decode(image_b64)
        mask_bytes = base64.b64decode(mask_b64) if mask_b64 else None
    except Exception:
        return make_error_response("Invalid base64 image or mask encoding", 400)

    provider = OpenAIImageProvider(api_key=api_key)
    try:
        image_url = provider.edit_image(
            prompt=prompt,
            image_bytes=image_bytes,
            mask_bytes=mask_bytes,
            model=model,
        )
        return jsonify({"image_url": image_url}), 200
    except Exception as e:
        return make_error_response(str(e), 500)
