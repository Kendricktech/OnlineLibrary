from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser
from .forms import CustomUserCreationForm  # Use the custom form

class CustomUserCreateView(CreateView):
    model = CustomUser
    template_name = "accounts/signup.html"
    form_class = CustomUserCreationForm  # Use the custom form with `role` and `subscription_type`
    success_url = reverse_lazy('dashboard')  # Redirect after successful signup
