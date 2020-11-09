import requests

from django.db import models
from django.db.models.signals import pre_save

from .utils import get_data, get_field

class Word(models.Model):
    word = models.CharField(max_length=100, unique=True)
    definition = models.CharField(max_length=1000, null=True, blank=True)
    synonyms = models.CharField(max_length=1000, null=True, blank=True)
    examples = models.CharField(max_length=1000, null=True, blank=True)
    type_of = models.CharField(max_length=1000, null=True, blank=True)
    is_meaningful = models.BooleanField(default=True)

    def __str__(self):
        return self.word

class ChatID(models.Model):
    chat_id = models.IntegerField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    words = models.ManyToManyField('Word', related_name='chatids', blank=True)

    def __str__(self):
        return str(self.chat_id)

def word_pre_save_reciver(sender, instance, *args, **kwargs):
    data = get_data(instance.word)
    definition = get_field("definition", data)
    if not definition:
        instance.is_meaningful = False
    instance.definition = definition
    synonyms = get_field("synonyms", data)
    examples = get_field("examples", data)
    type_of = get_field("typeOf", data)
    if synonyms and type(synonyms) == list:
        instance.synonyms = ','.join(synonyms)
    if examples and type(examples) == list:
        instance.examples = ','.join(examples)
    if type_of and type(type_of) == list:
        instance.type_of = ','.join(type_of)

pre_save.connect(word_pre_save_reciver, sender=Word)