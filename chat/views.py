from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from .models import Message
from django.utils import timezone
from django.urls import reverse
from notifications.models import Notification  # 1. Import your Notification model

@login_required
def chat_room(request, user_id):
    """Initial page load: gets the last 20 messages."""
    other_user = get_object_or_404(User, id=user_id)
    
    # When a user opens the chat room, automatically clear out unread notifications from this specific sender
    Notification.objects.filter(
        user=request.user,
        notification_type='new_message',
        text__contains=other_user.username
    ).delete() # Or set to is_read=True, but deleting keeps the database clean
    
    # Get last 20 messages for the conversation
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user) | 
         Q(sender=other_user, receiver=request.user))
    ).order_by('-timestamp')[:20]
    
    # We want them in chronological order (oldest at top)
    messages = reversed(messages)

    return render(request, 'chat/chat_room.html', {
        'other_user': other_user,
        'chat_messages': messages
    })

@login_required
def get_new_messages(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    last_id = request.GET.get('last_id')
    before_id = request.GET.get('before_id') 

    more_history = False

    # Handle Scrolling Up (History)
    if before_id:
        msgs_query = Message.objects.filter(
            (Q(sender=request.user, receiver=other_user) | 
             Q(sender=other_user, receiver=request.user)),
            id__lt=before_id
        ).order_by('-timestamp')[:20]
        
        # Check if there's potentially more after this batch
        more_history = msgs_query.count() == 20
        # Flip back to chronological so they prepend in order
        msgs = reversed(msgs_query)
    
    # Handle Regular Pinging (New Messages)
    else:
        msgs = Message.objects.filter(
            sender=other_user,
            receiver=request.user,
            id__gt=last_id
        ).order_by('timestamp')
        
        # If they are currently in the chat actively pinging and receiving messages, 
        # make sure we clear out any stray unread message notifications
        if msgs.exists():
            msgs.update(is_read=True)
            Notification.objects.filter(
                user=request.user,
                notification_type='new_message',
                text__contains=other_user.username
            ).delete()

    is_online = timezone.now() - other_user.profile.last_seen < timezone.timedelta(seconds=10)

    results = []
    for msg in msgs:
        results.append({
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender.username,
            "timestamp": msg.timestamp.strftime("%H:%M")
        })

    return JsonResponse({
        "messages": results,
        "friend_is_online": is_online,
        "more_history": more_history
    })

@login_required
def send_message(request, user_id):
    """AJAX: Handles sending a message."""
    if request.method == "POST":
        other_user = get_object_or_404(User, id=user_id)
        content = request.POST.get('content')
        if content:
            msg = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            
            # --- NOTIFICATION SYSTEM LOGIC ---
            # 2. Check if an UNREAD notification for a message from this sender already exists
            sender_display_name = request.user.username
            already_notified = Notification.objects.filter(
                user=other_user, 
                notification_type='new_message', 
                text__contains=f"({sender_display_name})",
                is_read=False
            ).exists()

            # 3. If no unread notification exists yet, create ONE single notification
            if not already_notified:
                sender_full_name = request.user.get_full_name() or request.user.username
                Notification.objects.create(
                    user=other_user,
                    notification_type='new_message',
                    text=f"New message from {sender_full_name} ({sender_display_name}).",
                    target_url=reverse('chat_room', args=[request.user.id])
                )
            # ---------------------------------

            return JsonResponse({
                "status": "sent",
                "id": msg.id,
                "content": msg.content,
                "timestamp": msg.timestamp.strftime("%H:%M")
            })
    return JsonResponse({"status": "error"}, status=400)