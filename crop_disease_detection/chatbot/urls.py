from django.urls import path
from .views import chatbot_view, chatbot_api

urlpatterns = [
    path('', chatbot_view, name='chatbot'),
    path('api/', chatbot_api, name='chatbot_api'),
]
