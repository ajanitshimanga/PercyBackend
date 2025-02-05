from typing import Optional
from api.llm import LLMFactory
from api.llm.models import OpenAIModels

class ChatCompletion:
    def __init__(self, system_prompt: str):
        self.llm_client = LLMFactory.create_client("openai")
        self.system_prompt = system_prompt
        self.conversation = [
            {"role": "system", "content": system_prompt}
        ]
    
    async def send_message(
        self,
        message: str,
        model: str = OpenAIModels.default().value,
        temperature: float = 1,
        max_tokens: int = 10000
    ) -> str:
        self.conversation.append({"role": "user", "content": message})
        
        response = await self.llm_client.get_chat_completion(
            messages=self.conversation,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        self.conversation.append({"role": "assistant", "content": response})
        return response 