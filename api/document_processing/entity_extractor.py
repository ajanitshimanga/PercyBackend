from typing import List, Dict
from api.llm.chat import ChatCompletion
import logging
import json

logger = logging.getLogger(__name__)

class EntityExtractor:
    def __init__(self):
        logger.info("Initializing EntityExtractor")
        self.chat = ChatCompletion(
            system_prompt=(
                "You are an expert at identifying living entities (characters, animals, insects) in text. "
                "You must ALWAYS respond with valid JSON and nothing else. "
                "Format your response exactly like this example:\n"
                '{\n'
                '    "characters": [\n'
                '        {\n'
                '            "name": "Example Name",\n'
                '            "type": "human",\n'
                '            "mentions": 1\n'
                '        }\n'
                '    ],\n'
                '    "metadata": {\n'
                '        "total_entities": 1,\n'
                '        "categories": ["human"]\n'
                '    }\n'
                '}\n\n'
                "Rules:\n"
                "1. Only use double quotes for JSON properties\n"
                "2. 'type' must be one of: human, bee, insect, animal\n"
                "3. 'mentions' must be a number\n"
                "4. Response must be pure JSON with no additional text"
            )
        )
    
    async def extract_entities(self, text: str) -> Dict:
        """Extract living entities from text using LLM"""
        logger.info("Processing text in single request")
        response = await self.chat.send_message(
            "Extract and categorize all living entities from this text. "
            "Remember to respond with ONLY valid JSON:\n\n" + text
        )
        
        try:
            # Try to clean the response if it's not pure JSON
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            entities_data = json.loads(response)
            logger.info(f"Found {entities_data['metadata']['total_entities']} entities "
                       f"across {len(entities_data['metadata']['categories'])} categories")
            return entities_data
        except json.JSONDecodeError as e:
            logger.error(f"Raw response: {response}")
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError("LLM response was not valid JSON")
