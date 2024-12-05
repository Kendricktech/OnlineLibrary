from django.contrib.auth.models import AbstractUser
from django.db import models
from books.models import Book  # Ensure you import the Book model correctly
class CustomUser(AbstractUser):
    image = models.ImageField(blank=True, null=True, default='media/uploads/users/images/default.png')
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    ]
    
    SUBSCRIPTION_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    is_premium = models.BooleanField(default=False)
    subscription_type = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        choices=SUBSCRIPTION_CHOICES
    )
    subscription_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
