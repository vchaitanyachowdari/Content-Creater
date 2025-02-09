from typing import Dict, Any
import asyncio
import logging
from pathlib import Path

from agents.content_engine import ContentEngine
from utils.config import Config
from utils.logger import setup_logger

class ChiatuAI:
    """
    Next-Gen AI Content Creation Engine
    Features:
    - Trend Analysis & Viral Content Generation
    - Fact Checking & Verification
    - Engaging Storytelling
    - Visual & Interactive Content
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = Config(config_path)
        self.logger = setup_logger()
        self.engine = ContentEngine(self.config)

    async def create_content(self, topic: str, preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create comprehensive content with all features
        """
        try:
            self.logger.info(f"Starting content creation for topic: {topic}")
            
            # Default preferences if none provided
            if preferences is None:
                preferences = {
                    "style": "engaging",
                    "tone": "professional",
                    "target_audience": "general",
                    "include_visuals": True,
                    "fact_check_level": "thorough"
                }

            # Generate content through the engine
            result = await self.engine.generate_content(topic, preferences)
            
            self.logger.info("Content creation completed successfully")
            return result

        except Exception as e:
            self.logger.error(f"Content creation failed: {e}")
            raise

async def main():
    # Initialize the AI engine
    chaitu = ChiatuAI()
    
    # Example content creation
    topic = "The Future of Artificial Intelligence in Healthcare"
    preferences = {
        "style": "engaging",
        "tone": "professional",
        "target_audience": "healthcare professionals",
        "include_visuals": True,
        "fact_check_level": "thorough"
    }
    
    try:
        result = await chaitu.create_content(topic, preferences)
        
        print("\n=== Generated Content ===")
        print(f"Title: {result['title']}")
        print(f"Word Count: {result['stats']['word_count']}")
        print(f"Reading Time: {result['stats']['reading_time']} minutes")
        print(f"Credibility Score: {result['stats']['credibility_score']}/10")
        print(f"Engagement Score: {result['stats']['engagement_score']}/10")
        print("\nContent Preview:")
        print(result['content'][:500] + "...\n")
        print(f"Generated {len(result['visuals'])} visuals")
        print(f"Added {len(result['interactive_elements'])} interactive elements")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 