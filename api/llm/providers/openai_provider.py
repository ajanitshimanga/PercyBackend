from typing import List, Dict, Any
from openai import AsyncOpenAI
from ..base import LLMClient
from ..models import OpenAIModels

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def get_completion(self,
                           prompt: str,
                           model: str = OpenAIModels.default().value,
                           temperature: float = 1,
                           max_tokens: int = 10000) -> str:
        response = await self.client.completions.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    
    async def get_chat_completion(self,
                                messages: List[Dict[str, str]],
                                model: str = OpenAIModels.default().value,
                                temperature: float = 1,
                                max_tokens: int = 10000) -> str:
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
