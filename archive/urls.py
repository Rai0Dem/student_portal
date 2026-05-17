from django.urls import path
from . import views


urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('my-uploads/', views.my_uploads, name='my_uploads'),
    path('edit/<int:file_id>/', views.edit_file, name='edit_file'),
]