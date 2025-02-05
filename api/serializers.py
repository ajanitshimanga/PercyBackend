from rest_framework import serializers
from .models import Item
from .llm.models import OpenAIModels

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class LLMChatRequestSerializer(serializers.Serializer):
    messages = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            required=True
        ),
        required=True
    )
    model = serializers.ChoiceField(
        choices=[model.value for model in OpenAIModels],
        default=OpenAIModels.default().value
    )
    temperature = serializers.FloatField(default=1, min_value=0, max_value=1)
    max_tokens = serializers.IntegerField(default=10000, min_value=1, max_value=10000)

    def validate_messages(self, value):
        for message in value:
            if not all(key in message for key in ['role', 'content']):
                raise serializers.ValidationError(
                    "Each message must contain 'role' and 'content' keys"
                )
            if message['role'] not in ['system', 'user', 'assistant']:
                raise serializers.ValidationError(
                    "Message role must be one of: system, user, assistant"
                )
        return value
