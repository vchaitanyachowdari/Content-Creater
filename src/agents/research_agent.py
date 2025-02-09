from typing import Dict, Any
from .base_agent import BaseAgent
import asyncio
from datetime import datetime
from src.utils.duckduckgo_search import DuckDuckGoSearch  # Correct import path

class ResearchAgent(BaseAgent):
    def __init__(self, model):
        self.model = model
        self.search_engine = DuckDuckGoSearch()  # Initialize search engine
    
    async def gather_information(self, topic: str) -> str:
        prompt = f"""
        Provide comprehensive information about: {topic}
        Include:
        - Key concepts and definitions
        - Important facts and statistics
        - Recent developments
        - Different viewpoints
        
        Format the response with bullet points and clear sections.
        """
        return await self.model.generate_content(prompt)
    
    async def analyze_perspectives(self, topic: str) -> str:
        prompt = f"""
        Analyze different perspectives on: {topic}
        Consider:
        - Various stakeholder viewpoints
        - Pros and cons
        - Potential controversies
        - Expert opinions
        """
        return await self.model.generate_content(prompt)

    async def validate_information(self, info: str) -> bool:
        # Implement a simple validation check (this can be expanded)
        # For example, check for the presence of key facts or references
        return "important" in info.lower()  # Placeholder for actual validation logic
    
    async def process_request(self, query: str) -> Dict[str, Any]:
        # Perform a search
        search_results = self.search_engine.search(query)
        
        # Gather information and analyze perspectives
        tasks = [
            self.gather_information(query),
            self.analyze_perspectives(query)
        ]
        info, perspectives = await asyncio.gather(*tasks)

        # Validate gathered information
        if not await self.validate_information(info):
            raise ValueError("Gathered information does not meet quality standards.")
        
        # Combine search results with gathered information
        combined_content = f"{info}\n\n{perspectives}\n\nSearch Results:\n" + "\n".join([f"{result['title']}: {result['href']}" for result in search_results])
        
        return {
            "type": "research",
            "content": combined_content,
            "metadata": {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "search_results": search_results  # Include search results in metadata
            }
        } 