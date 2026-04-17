from django.urls import path
from .views import chat_with_ai, ChatHistoryView

urlpatterns = [
    path('chat/', chat_with_ai, name='ai-chat'),
    path('history/', ChatHistoryView.as_view(), name='chat-history'),
]
