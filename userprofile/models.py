from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    # Role choices
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, max_length=350)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


    last_seen = models.DateTimeField(default=timezone.now)

    def is_online(self):
        now = timezone.now()
        return now - self.last_seen < timezone.timedelta(seconds=6)
    
    def __str__(self):\
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
