import json

from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework import status, viewsets, filters

from .serializers import WordSerializer, ChatIDSerializer

from main.models import Word, ChatID


class ChatIDViewSet(viewsets.ModelViewSet):
    """
    List all workers, or create a new worker.
    """
    queryset = ChatID.objects.all()
    filter_backends = [filters.OrderingFilter]
    serializer_class = ChatIDSerializer
    lookup_field = 'chat_id'

    def destroy(self, request, *args, **kwargs):
        return super(ChatIDViewSet, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        chat_id = request.data.get('chat_id')
        name = request.GET.get("name")
        username = request.GET.get("username")
        chat_obj = ChatID.objects.filter(chat_id__iexact=chat_id).first()
        if chat_id and (not chat_obj or (not (chat_obj.name and chat_obj.username))):
            chat_new_obj, chat_new_obj_created = ChatID.objects.get_or_create(chat_id=chat_id)
            if name and username and not (chat_new_obj.name and chat_new_obj.username):
                chat_new_obj.name = name
                chat_new_obj.username = username
                chat_new_obj.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="Database already created")

class WordViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']
    lookup_field = 'word'

    def get_words_by_chatid(self, chat_id):
        chat_obj = ChatID.objects.filter(chat_id__iexact=chat_id)
        if chat_obj.exists():
            return chat_obj.first().words.all()
        return

    def list(self, request):
        queryset = Word.objects.all()
        chat_id = request.GET.get("chatid")
        meaningful = request.GET.get("meaningful")
        word = request.GET.get("word")
        if word and chat_id and not meaningful:
            word_obj = Word.objects.filter(word__iexact=word).first()
            if word_obj and word_obj.chatids.filter(chat_id__iexact=chat_id).exists():
                queryset = word_obj
                serializer = WordSerializer(queryset)
                return Response(serializer.data)
        if chat_id and (word == None) and not meaningful:
            queryset = self.get_words_by_chatid(chat_id)
            if not queryset:
                return Response(status=status.HTTP_404_NOT_FOUND, data="Word not found")
            serializer = WordSerializer(queryset, many=True)
            return Response(serializer.data)
        if chat_id and meaningful:
            print("yo")
            word_obj = self.get_words_by_chatid(chat_id)
            if word_obj:
                queryset = word_obj.filter(is_meaningful=meaningful)
                print(queryset)
                serializer = WordSerializer(queryset, many=True)
                return Response(serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND, data="Word not found")
        if not (chat_id and word):
            serializer = WordSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND, data="Word not found")

    def destroy(self, request, *args, **kwargs):
        chat_id = request.GET.get("chatid")
        obj = self.get_object()
        if obj and chat_id:
            chat_obj = ChatID.objects.filter(chat_id__iexact=chat_id)
            if chat_obj.exists():
                chat_obj = chat_obj.first()
                chat_obj.words.remove(obj)
                return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def create(self, request, *args, **kwargs):
        chat_id = request.GET.get('chatid')
        word = request.data.get("word")
        word_obj = None
        if chat_id and word:
            word_obj, word_obj_created = Word.objects.get_or_create(word=word)
            if not word_obj_created:
                word_already_created = word_obj.chatids.filter(chat_id__iexact=chat_id).exists()
                if word_already_created:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="Word is already created")
            chat_obj, chat_obj_created = ChatID.objects.get_or_create(chat_id=chat_id)
            chat_obj.words.add(word_obj)
        return Response(status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     chat_id = self.request.GET.get("chatid")
    #     print(chat_id)
    #     chatid = ChatID.objects.all().filter(chat_id__iexact=chat_id)
        
# class WordAPIView(mixins.CreateModelMixin,
#                 mixins.RetrieveModelMixin,
#                 mixins.DestroyModelMixin,
#                  generics.ListAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Word.objects.all()
#     serializer_class = WordSerializer
#     lookup_field = 'word'

#     def delete(self, request, format=None):
#         word = request.GET.get("word")
#         if word:
#             snippet = Word.objects.all().filter(word__iexact=word)
#         chat_id = request.GET.get("chat_id")
#         snippet = Word.objects.all().filter(word__chat_id)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def get_queryset(self):
#         request = self.request
#         qs = Word.objects.all()
#         query = request.GET.get('q')
#         chat_id = request.GET.get('chat_id')
#         word = request.GET.get('word')
#         if chat_id:
#             qs = qs.filter(chat_id__iexact=chat_id)
#         if query:
#             qs = qs.filter(word__icontains=query)
#         if word:
#             qs = qs.filter(word__iexact=word)
#         return qs
    
#     def get_id_by_field(self, field, field_data):
#         if field=="word":
#             return Word.objects.all().filter(word__iexact=field_data).first().id
#         if field=="chat_id":
#             return Word.objects.all().filter(chatid__iexact=field_data).first().id

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def get_object(self):
#         request = self.request
#         passed_chat_id = request.GET.get('chat_id', None)
#         queryset = self.get_queryset()
#         id = self.get_id_by_field("chat_id", passed_chat_id)
#         obj = None
#         if passed_chat_id:
#             obj = get_object_or_404(queryset, id=id)
#             self.check_object_permissions(request, obj)
#         print(obj)
#         return obj

#     def perform_create(self, serializer):
#         chat_id = self.request.GET.get("chat_id")
#         words = Word.objects.all()
#         if chat_id:
#             serializer.save(chat_id=chat_id)

# class WordAPIDeleteView(generics.DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Word.objects.all()
#     serializer_class = WordSerializer
#     lookup_field = 'word'