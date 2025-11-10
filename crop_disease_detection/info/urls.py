from django.urls import path
from . import views

urlpatterns = [
    path('', views.disease_info_view, name='disease_info'),
]
