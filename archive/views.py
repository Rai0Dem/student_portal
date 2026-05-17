from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test # Add user_passes_test here
from .models import SharedFile
from django.urls import reverse
from notifications.models import Notification
from .forms import FileUploadForm
import os

@login_required
def file_list(request):
    Notification.objects.filter(user=request.user, notification_type='file_upload').delete()
    files = SharedFile.objects.all()

    # 1. Search Logic
    query = request.GET.get('q')
    if query:
        files = files.filter(title__icontains=query)

    # 2. Filter by Friends (Teachers)
    filter_friends = request.GET.get('friends')
    if filter_friends == 'true':
        # Since 'friends' is directly on the User model:
        friend_users = request.user.friends.all()
        files = files.filter(uploader__in=friend_users)

    # 3. Sorting
    sort = request.GET.get('sort', 'alphabetical')
    if sort == 'newest':
        files = files.order_by('-uploaded_at')
    else:
        files = files.order_by('title')

    return render(request, 'archive/file_list.html', {'files': files})

def is_teacher(user):
    return hasattr(user, 'profile') and user.profile.role == 'teacher'

@login_required
@user_passes_test(is_teacher, login_url='home')
def my_uploads(request):
    # Only get files uploaded by THIS user
    files = SharedFile.objects.filter(uploader=request.user).order_by('-uploaded_at')
    
    return render(request, 'archive/my_uploads.html', {'files': files})


@login_required
@user_passes_test(is_teacher, login_url='home')
def edit_file(request, file_id):
    file_instance = get_object_or_404(SharedFile, id=file_id, uploader=request.user)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            # 1. Get the physical path of the file on your computer
            if file_instance.file:
                if os.path.isfile(file_instance.file.path):
                    os.remove(file_instance.file.path) # 2. Delete the physical file
            
            # 3. Delete the database record
            file_instance.delete()
            return redirect('my_uploads')
            
        form = FileUploadForm(request.POST, request.FILES, instance=file_instance)
        if form.is_valid():
            # Optional: If they are UPDATING the file, you might want to 
            # delete the old physical file here too so you don't keep both.
            form.save()
            return redirect('my_uploads')
    else:
        form = FileUploadForm(instance=file_instance)
        
    return render(request, 'archive/edit_file.html', {'form': form, 'file': file_instance})

@login_required
@user_passes_test(is_teacher, login_url='home')
def upload_file(request):
    if request.method == 'POST':
        # request.FILES is required for uploading files!
        form = FileUploadForm(request.POST, request.FILES) 
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.uploader = request.user # Set the current user as the owner
            new_file.save()
            # --- TRIGGER NOTIFICATIONS FOR FRIENDS ---
            friend_users = request.user.friends.all() # Pulls friend instances from your user profile model logic
            for friend in friend_users:
             Notification.objects.create(
             user=friend,
             notification_type='file_upload',
             text=f"Teacher {request.user.get_full_name() or request.user.username} uploaded a new file: {new_file.title}",
             target_url=reverse('file_list')
            )
            return redirect('file_list') # Go back to the archive after success
    else:
        form = FileUploadForm()
    
    return render(request, 'archive/upload_file.html', {'form': form})