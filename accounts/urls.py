from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import CustomUserCreateView

app_name = 'accounts'

urlpatterns = [
    # Default auth URLs
    path('accounts/', include('django.contrib.auth.urls')),  # This includes login, logout, password change, etc.
    
    # Custom login view with redirect to the dashboard for authenticated users
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, next_page='dashboard'), name='login'),

    # Dashboard view
        path('signup/', CustomUserCreateView.as_view(), name='signup'),

    # Optionally add registration if you have a custom user creation view
    path('register', CustomUserCreateView.as_view(), name='register'),
]
