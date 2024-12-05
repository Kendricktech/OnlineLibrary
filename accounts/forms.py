from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2', 
            'role', 
            'subscription_type'
        ]
        widgets = {
            'role': forms.Select(attrs={
                'class': 'select select-bordered w-full bg-base-100 '
            }),
            'subscription_type': forms.Select(attrs={
                'class': 'select select-bordered w-full bg-base-100'
            }),
        }

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in ['student', 'teacher', 'librarian', 'admin']:
            raise forms.ValidationError("Invalid role selected.")
        return role
