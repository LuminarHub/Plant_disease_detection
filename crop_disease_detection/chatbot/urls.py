from django.urls import path
from .views import chatbot_view

urlpatterns = [
    path('', chatbot_view, name='chatbot'),  # Single endpoint handles both GET (UI) and POST (chat)
]
