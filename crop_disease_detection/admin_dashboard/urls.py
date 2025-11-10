from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.users_list, name='admin_users'),
    path('feedbacks/', views.feedbacks_list, name='admin_feedbacks'),
]
