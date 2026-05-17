from django.db import models
from django.contrib.auth.models import User
import os

class SharedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='archive/files/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title'] # Default alphabetical order

    def __str__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def size_mb(self):
        """Returns file size in MB rounded to 2 decimals."""
        try:
            return round(self.file.size / (1024 * 1024), 2)
        except:
            return 0