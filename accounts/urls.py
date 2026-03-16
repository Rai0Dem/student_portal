from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("search/", views.search_users, name="search_users"),
    path("ping/", views.update_last_seen, name="update_last_seen"),
]