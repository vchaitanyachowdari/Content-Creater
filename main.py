#!/usr/bin/env python3
"""
ChiatuAI: Advanced Content Generation System
Author: V Chaitanya Chowdari
"""
import os
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any
from src.agents.content_engine import ContentEngine
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.services.slack_service import SlackService
from dotenv import load_dotenv
from your_main_module import app  # Import your Flask or FastAPI app

# Load environment variables
load_dotenv()

def main():
    """Main execution function"""
    try:
        # Initialize AI system
        logger = setup_logger()
        config = Config()
        engine = ContentEngine(config)
        
        # Initialize and start Slack service
        slack_service = SlackService(engine)
        slack_service.start()
        
        logger.info("ChiatuAI Slack bot is running. Use !generate command in Slack to generate content.")
        
        # Keep the application running
        while True:
            pass
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)