import io
import time
from openai import OpenAI
from typing import List, Dict, Union
from utils.logger import logger
from utils.config import OPENROUTER_API_KEY, OPENROUTER_MODEL


class LLMService:
  def __init__(self):
    self.client = OpenAI(
      base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY
    )
    self.model = OPENROUTER_MODEL

  def chat_completions(
    self,
    prompt: str = None,
    image: Union[io.BytesIO, bytes, str] = None,
    messages: Union[str, List[Dict[str, str]]] = None,
    temperature: float = 0.6,
    max_tokens: int = 512,
  ) -> str:
    try:
      mock_usage = type("Usage", (), {"prompt_tokens": 0, "total_tokens": 0})()

      if image:
        image_url = image if isinstance(image, str) else self._to_base64_data_uri(image)
        content = [
          {"type": "text", "text": prompt or "Describe this image."},
          {"type": "image_url", "image_url": {"url": image_url}},
        ]
        chat_messages = [{"role": "user", "content": content}]
      elif messages:
        chat_messages = (
          [{"role": "user", "content": messages}]
          if isinstance(messages, str)
          else messages
        )
      elif prompt:
        chat_messages = [{"role": "user", "content": prompt}]
      else:
        return "⚠️ No input provided.", mock_usage

      api_params = {
        "model": self.model,
        "messages": chat_messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
      }

      api_params["tool_choice"] = "none"
      response = self.client.chat.completions.create(**api_params)
      message = response.choices[0].message
      return message.content.strip(), response.usage
    except Exception as e:
      ### 429 + Retry time
      if hasattr(e, "response") and getattr(e.response, "status_code", None) == 429:
        headers = getattr(e.response, "headers", {})
        reset_ts = int(headers.get("X-RateLimit-Reset", "0"))
        current_ts = int(time.time())
        wait_sec = max(0, reset_ts - current_ts)

        mins = wait_sec // 60
        secs = wait_sec % 60
        formatted = f"{mins}m {secs}s" if mins else f"{secs}s"

        return (
          f"⏳ You've hit the rate limit for this model. Try again in {formatted}.",
          mock_usage,
        )

      ### Catch all
      logger.error(f"Unexpected error in chat_completions: {e}")
      return "😵 Something went wrong while generating a response.", mock_usage
