from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class HuggingFaceModel:
    def __init__(self, model_name: str):
        self.model = pipeline("text-generation", model=model_name)
    
    async def improve_content(self, prompt: str) -> str:
        """Improve content using Hugging Face model"""
        try:
            response = self.model(prompt, max_length=150)  # Adjust max_length as needed
            return response[0]['generated_text']
        except Exception as e:
            logger.error(f"Hugging Face model error: {str(e)}")
            return None 