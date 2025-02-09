from .duckduckgo_search import DuckDuckGoSearch
import logging

logger = logging.getLogger(__name__)

class DuckDuckGoSearch:
    def __init__(self):
        pass

    def search(self, query: str):
        """Perform a search using DuckDuckGo"""
        try:
            results = DuckDuckGoSearch().search(query)  # Adjust max_results as needed
            return results
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {str(e)}")
            return [] 