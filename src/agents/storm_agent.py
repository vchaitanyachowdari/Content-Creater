from typing import Dict, Any
from src.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class StormAgent(BaseAgent):
    def __init__(self, model):
        self.model = model

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Extract topic
            topic = request.get('content', '')
            if not topic:
                raise ValueError("Empty content in request")
            
            # Create prompt with proper string formatting
            prompt = (
                f"Write a comprehensive article about: {topic}\n\n"
                "Structure:\n"
                "1. Introduction\n"
                "   * Overview and importance\n"
                "   * Key points to be covered\n\n"
                "2. Main Discussion\n"
                "   * Key concepts and explanations\n"
                "   * Supporting evidence\n"
                "   * Examples and applications\n\n"
                "3. Analysis\n"
                "   * Different perspectives\n"
                "   * Current developments\n"
                "   * Future implications\n\n"
                "4. Conclusion\n"
                "   * Summary of main points\n"
                "   * Final insights\n\n"
                "Requirements:\n"
                "- Use clear headings and bullet points\n"
                "- Include specific examples\n"
                "- Maintain professional tone\n"
                "- Focus on clarity and accuracy"
            )
            
            # Generate content
            content = await self.model.generate_content(prompt)
            if not content:
                raise ValueError("Failed to generate content")
            
            return {
                "type": "storm_article",
                "content": str(content).strip(),
                "metadata": {
                    **request.get('metadata', {}),
                    "article_type": "comprehensive"
                }
            }
            
        except Exception as e:
            logger.error(f"StormAgent error: {str(e)}")
            raise