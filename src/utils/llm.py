import os
import httpx
import asyncio

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-4-maverick")

async def generate_response(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "http://localhost",  
                    "X-Title": "BooetteBot",
                },
                json={
                    "model": OPENROUTER_MODEL,
                    "messages": [
                        {"role": "system", "content": "You are Booette, a cute, witty, girly pop-core and friendly Discord bot."},
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": 150,
                }
            )
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Oops, something went wrong: {e}"
