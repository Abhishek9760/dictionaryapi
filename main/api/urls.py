from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework import routers

from .views import WordViewSet, ChatIDViewSet

router = DefaultRouter()
router.register(r'api/chatid', ChatIDViewSet, basename='chat_id')
router.register(r'api/word', WordViewSet, basename='word')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework')),
    # path("", WordAPIView.as_view()),
    # path("delete/<str:word>/", WordAPIDeleteView.as_view()),
]
