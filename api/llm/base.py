from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMClient(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    def __init__(self, api_key: str):
        pass
    
    @abstractmethod
    async def get_completion(self, 
                           prompt: str,
                           model: str,
                           temperature: float = 1,
                           max_tokens: int = 10000) -> str:
        """Get completion from LLM"""
        pass
    
    @abstractmethod
    async def get_chat_completion(self,
                                messages: List[Dict[str, str]],
                                model: str,
                                temperature: float = 1,
                                max_tokens: int = 10000) -> str:
        """Get chat completion from LLM"""
        pass
