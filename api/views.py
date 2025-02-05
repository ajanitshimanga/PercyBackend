from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Item
from api.serializers import ItemSerializer, LLMChatRequestSerializer
from api.llm import LLMFactory
from api.llm.models import OpenAIModels
import asyncio

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
