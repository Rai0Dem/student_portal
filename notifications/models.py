from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('friend_request', 'Friend Request'),
        ('new_message', 'New Message'),
        ('file_upload', 'File Upload'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    text = models.TextField()
    target_url = models.CharField(max_length=255) # Where the button redirects you
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at'] # Newest first

    def __str__(self):
        return f"{self.user.username} - {self.notification_type} - {self.created_at}"