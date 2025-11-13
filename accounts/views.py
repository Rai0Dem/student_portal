from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm

# SIGNUP FUNCTION
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()            # Save new user to the database
            login(request, user)          # Log them in immediately
            return redirect('home')       # Send them to the home page
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# LOGIN FUNCTION
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()        # Get the user who logged in
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# LOGOUT FUNCTION
def logout_view(request):
    logout(request)
    return redirect('login')
