from duckduckgo_search import DDGS
import logging

logger = logging.getLogger(__name__)

class DuckDuckGoSearch:
    def __init__(self):
        self.ddgs = DDGS()
    
    def search(self, query: str, max_results: int = 5):
        """Perform a search using DuckDuckGo"""
        try:
            return self.ddgs.text(query, max_results=max_results)
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {str(e)}")
            return [] 