import os
from typing import Optional
from .base import LLMClient
from .providers.openai_provider import OpenAIClient

class LLMFactory:
    @staticmethod
    def create_client(provider: str = "openai", api_key: Optional[str] = None) -> LLMClient:
        if provider == "openai":
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found")
            return OpenAIClient(api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
