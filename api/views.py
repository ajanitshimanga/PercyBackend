from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Item
from api.serializers import ItemSerializer, LLMChatRequestSerializer, DocumentProcessingSerializer
from api.llm import LLMFactory
from api.llm.models import OpenAIModels
from api.document_processing.pipeline import DocumentProcessingPipeline
import asyncio
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class LLMViewSet(viewsets.ViewSet):
    serializer_class = LLMChatRequestSerializer

    @action(detail=False, methods=['post'])
    def chat(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create LLM client
            llm_client = LLMFactory.create_client("openai")
            
            # Get response from LLM
            response = asyncio.run(
                llm_client.get_chat_completion(
                    messages=serializer.validated_data['messages'],
                    model=serializer.validated_data['model'],
                    temperature=serializer.validated_data['temperature'],
                    max_tokens=serializer.validated_data['max_tokens']
                )
            )
            
            return Response({
                'response': response,
                'model': serializer.validated_data['model']
            })

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DocumentProcessingViewSet(viewsets.ViewSet):
    serializer_class = DocumentProcessingSerializer

    @action(detail=False, methods=['post'])
    def extract_entities(self, request):
        logger.info("Starting entity extraction request")
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Invalid request data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            logger.info(f"Processing file: {serializer.validated_data['filename']}")
            pipeline = DocumentProcessingPipeline()
            
            # Use async_to_sync with a timeout
            entities_data = async_to_sync(pipeline.process_document)(
                serializer.validated_data['filename']
            )
            
            logger.info(f"Successfully processed document")
            return Response(entities_data)

        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            return Response(
                {'error': 'File not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            logger.error(f"Invalid response format: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
