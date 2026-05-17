from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import FriendRequest
from notifications.models import Notification
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q

@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    if request.user == receiver:
        return redirect('search_users')

    # 1. Look for ANY existing request (Accepted or Pending) between these two
    existing_request = FriendRequest.objects.filter(
        Q(sender=request.user, receiver=receiver) | 
        Q(sender=receiver, receiver=request.user)
    )

    if existing_request.exists():
        # If the request was already accepted (they were friends before)
        # or if it's pending, we clear it so we can start fresh.
        existing_request.delete()

    # 2. Now create the clean, new request
    FriendRequest.objects.create(sender=request.user, receiver=receiver)

# Inside your send_request view logic:
    Notification.objects.create(
    user=receiver, # The person receiving the request
    notification_type='friend_request',
    text=f"{request.user.get_full_name() or request.user.username} sent you a friend request.",
    target_url=reverse('incoming_requests') # Update with your exact friend request list URL name
)

    return redirect('search_users')


@login_required
def accept_friend_request(request, request_id):

    # Get the specific request object using its ID
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)

    # Add to friends list (Assuming you have a ManyToManyField named 'friends' on your User model)
    friend_request.sender.friends.add(request.user)
    request.user.friends.add(friend_request.sender)

    # Mark as accepted
    friend_request.accepted = True
    friend_request.save()

    return redirect('incoming_requests')

@login_required
def decline_friend_request(request, request_id):
    # Find the request where the current user is the intended receiver
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    
    # Simply delete the request from the database
    friend_request.delete()
    
    # Redirect back to the requests page
    return redirect('incoming_requests')

@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    
    # Remove from many-to-many relationship
    request.user.friends.remove(friend)
    friend.friends.remove(request.user)

    # Delete the FriendRequest record using Q objects
    # We use Q to say: "Delete if (I sent to them) OR (They sent to me)"
    FriendRequest.objects.filter(
        Q(sender=request.user, receiver=friend) | 
        Q(sender=friend, receiver=request.user)
    ).delete()

    return redirect('friends_list')

def incoming_friend_requests(request):
    Notification.objects.filter(user=request.user, notification_type='friend_request').delete()
    requests = FriendRequest.objects.filter(receiver=request.user, accepted=False)
    return render(request, 'friends/incoming_requests.html', {'requests': requests})

@login_required
def friends_list(request):
    friends = request.user.friends.all()
    return render(request, "friends/friends_list.html", {"friends": friends})


@login_required
def check_online(request):

    friends = request.user.friends.all()  # adjust if your relation differs

    data = {}

    for friend in friends:
        is_online = timezone.now() - friend.profile.last_seen < timezone.timedelta(seconds=10)
        data[friend.id] = is_online

    return JsonResponse(data)

@login_required
def view_profile(request, user_id):
    # Fetch the user whose profile we want to see
    target_user = get_object_or_404(User, id=user_id)
    return render(request, 'friends/view_profile.html', {'target_user': target_user})