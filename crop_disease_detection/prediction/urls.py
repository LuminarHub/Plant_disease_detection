from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_disease, name='prediction'),
    path('history/', views.prediction_history, name='history'),
]
