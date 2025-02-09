from google.generativeai import configure, GenerativeModel
import logging

class AIModel:
    """Model class for interacting with Google's Gemini API"""
    
    def __init__(self, api_key: str):
        self.logger = logging.getLogger(__name__)
        configure(api_key=api_key)
        self.model = GenerativeModel('gemini-pro')

    async def generate_content(self, prompt: str) -> str:
        """Generate content based on the provided prompt"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Content generation failed: {e}")
            raise 