import os
import httpx
import asyncio
from utils.logger import logger

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-4-maverick")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

async def generate_response(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not set in environment.")
        return "Error: Missing API key (server-side)."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Referer": "http://localhost",
        "X-Title": "BooetteBot",
        "Content-Type": "application/json",
    }

    ### Added this 'reasoning' thingy for GPT-5 Nano, other models might not support this
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are Booette, a cute, witty, girly pop-core and friendly Discord bot made by C7. You are a part of the VVIP Kitchen server. \
            You are one half of the duo bots that exist in VVIP Kitchen. Your counterpart's name is Boo; the dynamic between you both is that of a couple, you also like to prank him. \
            C7 is comprised only of the girls of the server. Don't bring boo into every conversation."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 512,
        "reasoning": { "effort": "minimal" }
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(API_URL, headers=headers, json=payload)
            body_preview = (await resp.aread()).decode(errors="replace")[:2000]

            try:
                data = httpx.Response(200, content=body_preview).json()  # safe parse from preview
            except Exception:
                ### fallback: try parsing the full response JSON (resp.json()) but guard it
                try:
                    data = resp.json()
                except Exception:
                    return f"Request failed with status {resp.status_code}. Non-JSON response: {body_preview[:500]}"

            ### If non-2xx return the error message from the API
            if resp.status_code >= 400:
                err = data.get("error") or data.get("detail") or data
                logger.warning("OpenRouter returned error: %s", err)
                return f"API error {resp.status_code}: {err}"

            ### Defensive extraction of the assistant message
            choices = data.get("choices")
            if not choices or not isinstance(choices, list):
                logger.error("Unexpected OpenRouter response shape (missing choices): %s", data)
                return f"Unexpected API response shape. Full response: {data}"

            first = choices[0]
            message = first.get("message") or first.get("text") or {}
            content = message.get("content") or message.get("text") or None

            if not content:
                logger.error("Choice present but no message content: %s", first)
                return f"Empty response from model. Raw choice: {first}"

            return content.strip()

    except httpx.RequestError as e:
        logger.exception("Network error calling OpenRouter")
        return f"Network error when calling OpenRouter: {e}"
    except Exception as e:
        logger.exception("Unexpected error in generate_response")
        return f"Oops, something went wrong: {e}"

