from typing import Dict
from .document_loader import DocumentLoader
from .entity_extractor import EntityExtractor
import logging

logger = logging.getLogger(__name__)

class DocumentProcessingPipeline:
    def __init__(self):
        self.loader = DocumentLoader()
        self.extractor = EntityExtractor()
    
    async def process_document(self, filename: str) -> Dict:
        """Process document and extract entities"""
        logger.info(f"Loading document: {filename}")
        # Load document
        text = self.loader.load_local(filename)
        
        logger.info("Starting entity extraction")
        # Extract entities
        entities_data = await self.extractor.extract_entities(text)
        
        logger.info(f"Extracted {entities_data['metadata']['total_entities']} entities "
                   f"across {len(entities_data['metadata']['categories'])} categories")
        return entities_data
