from django.urls import path
from .views import conversations_view, send_message_view, create_chat_view

urlpatterns = [
    path('conversations/', conversations_view, name='conversations'),
    path('chat/<int:chat_id>/send/', send_message_view, name='send_message'),
    path('chat/create/<int:user_id>/', create_chat_view, name='create_chat'),
]
