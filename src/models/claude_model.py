from anthropic import Anthropic
from typing import Any
import asyncio
import logging

class ClaudeModel:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    async def generate_content(self, prompt: str) -> str:
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            self.logger.error(f"Claude generation failed: {e}")
            raise 