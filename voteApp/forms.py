# voteApp/forms.py
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

class GenerateProxyVoteForm(forms.Form):
    expires_at = forms.DateTimeField(help_text="Enter the expiration date for the proxy vote key.")

    def clean_expires_at(self):
        expires_at = self.cleaned_data.get('expires_at')
        if expires_at < datetime.now():
            raise ValidationError("Expiration date cannot be in the past.")
        return expires_at