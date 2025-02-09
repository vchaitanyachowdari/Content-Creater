import google.generativeai as genai
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class GeminiModel:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_content(self, prompt: str) -> Optional[str]:
        """Generate content with better error handling"""
        try:
            if not isinstance(prompt, str):
                prompt = str(prompt)
            prompt = prompt.strip()
            
            response = await self.model.generate_content_async(prompt)
            
            if hasattr(response, 'text'):
                return response.text.strip()
            elif hasattr(response, 'parts'):
                parts = [str(part.text).strip() for part in response.parts if part.text]
                return ' '.join(parts)
            
            return None
            
        except Exception as e:
            logger.error(f"Gemini model error: {str(e)}")
            return None 