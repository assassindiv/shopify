import json

import httpx

from app.core.config import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL
from app.core.errors import AppError


def _extract_json(content: str) -> dict:
    cleaned = content.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.removeprefix("json").strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1:
        cleaned = cleaned[start : end + 1]

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AppError(
            code="AI_PARSE_ERROR",
            message="Groq returned a response that could not be parsed.",
            status_code=502,
        ) from exc


async def groq_chat_json(
    *,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0,
    max_tokens: int = 700,
) -> dict:
    if not GROQ_API_KEY:
        raise AppError(
            code="GROQ_API_KEY_MISSING",
            message="Set GROQ_API_KEY before using the AI chat endpoint.",
            status_code=503,
        )

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
    except httpx.HTTPError as exc:
        raise AppError(
            code="GROQ_REQUEST_FAILED",
            message="Could not reach Groq for the AI chat request.",
            status_code=502,
        ) from exc

    if response.status_code >= 400:
        raise AppError(
            code="GROQ_API_ERROR",
            message=f"Groq returned status {response.status_code}.",
            status_code=502,
        )

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return _extract_json(content)
