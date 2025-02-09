from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    @abstractmethod
    async def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process user request and return response"""
        pass 

    def clean_response(self, response: Optional[str]) -> str:
        """Clean and validate model response"""
        if not response:
            return ""
        return str(response).strip()
    
    def is_valid_response(self, response: str) -> bool:
        """Check if response is valid"""
        return bool(response and response.strip()) 