from django.urls import path
from . import views

urlpatterns = [
    path("list", views.friends_list, name="friends_list"),
    path("send/<int:user_id>/", views.send_friend_request, name="send_friend_request"),
    path("accept/<int:request_id>/", views.accept_friend_request, name="accept_friend_request"),
    path("remove/<int:user_id>/", views.remove_friend, name="remove_friend"),
    path('requests/', views.incoming_friend_requests, name='incoming_requests'),
    path("check-online/", views.check_online, name="check_online"),
    path("profile/<int:user_id>/", views.view_profile, name="view_profile"),
    path('requests/decline/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
]