
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserSignupForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from friends.models import FriendRequest
from django.http import JsonResponse
from django.utils import timezone


# SIGNUP FUNCTION
def signup_view(request):
    if request.method == 'POST':
        # Pass both POST and FILES for file uploads
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()          # Saves User

            # Now save profile fields
            profile = user.profile
            profile.role = form.cleaned_data['role']
            profile.bio = form.cleaned_data['bio']
            profile.birthdate = form.cleaned_data['birthdate']
            profile.gender = form.cleaned_data['gender']
            # Save avatar if provided
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.save()

            login(request, user)
            return redirect('home')
    else:
        form = UserSignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

# LOGIN FUNCTION
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()        # Get the user who logged in
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# LOGOUT FUNCTION
def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def search_users(request):

    query = request.GET.get("q", "").strip()

    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(username__icontains=query)

    # Remove existing friends
    users = users.exclude(id__in=request.user.friends.all())

    # Users I already sent requests to
    outgoing_requests = FriendRequest.objects.filter(
        sender=request.user,
        accepted=False
    ).values_list("receiver_id", flat=True)

    # Users who sent me requests
    incoming_requests = FriendRequest.objects.filter(
        receiver=request.user,
        accepted=False
    ).values_list("sender_id", flat=True)

    return render(
        request,
        "accounts/search_users.html",
        {
            "users": users,
            "query": query,
            "outgoing_requests": outgoing_requests,
            "incoming_requests": incoming_requests,
        }
    )

@login_required
def update_last_seen(request):
    user_profile = request.user.profile
    user_profile.last_seen = timezone.now()
    user_profile.save(update_fields=['last_seen'])
    return JsonResponse({"status": "ok"})