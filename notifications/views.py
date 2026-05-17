from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from notifications.models import Notification

@login_required
def notification_list(request):
    # Fetch all notifications for the logged-in user
    all_notifications = Notification.objects.filter(user=request.user)
    
    # Optional: Automatically mark them as read when the user views the page
    all_notifications.filter(is_read=False).update(is_read=True)

    # Paginate: Show 10 notifications per page
    paginator = Paginator(all_notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notifications/list.html', {'page_obj': page_obj})

@login_required
def unread_notification_count(request):
    # Counts all unread notifications for the logged-in user
    # Note: If your system deletes notifications when viewed instead of marking them read,
    # change this to: Notification.objects.filter(user=request.user).count()
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})