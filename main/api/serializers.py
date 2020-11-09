from rest_framework import serializers, status
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response

from main.models import Word, ChatID

from django.shortcuts import get_object_or_404


class ChatIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatID
        extra_kwargs = {'word': {'required': False}}
        fields = [
            'id',
            'words',
            'chat_id'
        ]
    
    # def create(self, validated_data):
    #     chat_id = validated_data.get('chat_id')
    #     chat_obj = ChatID.objects.filter(chat_id__iexact=chat_id)
    #     if chat_id and (not chat_obj.exists()):
    #         chat_new_obj = ChatID.objects.create(chat_id=chat_id)
    #         return chat_new_obj
    #     return chat_obj.first()


class WordSerializer(serializers.ModelSerializer):
    chatids = ChatIDSerializer(many=True, read_only=True)
    class Meta:
        model = Word
        fields = [
            'id',
            'chatids',
            'word',
            'definition',
            'synonyms',
            'examples',
            'type_of',
        ]

        extra_kwargs = {'chatids': {'required': False}}
    
    # def create(self, validated_data):
    #     request = self.context.get("request")
    #     chat_id = request.GET.get('chatid')
    #     word = validated_data.get("word")
    #     word_obj = None
    #     if chat_id:
    #         word_obj, created = Word.objects.get_or_create(word=word)
    #         print(word_obj)
    #         chat_obj, _ = ChatID.objects.get_or_create(chat_id=chat_id)
    #         chat_obj.words.add(word_obj)
    #     return word_obj
