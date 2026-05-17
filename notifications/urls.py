from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('api/unread-count/', views.unread_notification_count, name='unread_notification_count'),
]