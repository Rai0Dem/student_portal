from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.chat_room, name='chat_room'),
    path('api/get-messages/<int:user_id>/', views.get_new_messages, name='get_new_messages'),
    path('api/send-message/<int:user_id>/', views.send_message, name='send_message'),
]