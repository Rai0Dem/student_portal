from django import forms
from .models import SharedFile
import os

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['title', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            extension = os.path.splitext(file.name)[1].lower()
            if extension not in ['.pdf', '.txt']:
                raise forms.ValidationError("Only PDF and TXT files are allowed.")
        return file