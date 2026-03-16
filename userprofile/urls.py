from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("edit/", views.edit_profile, name="edit_profile"),
]