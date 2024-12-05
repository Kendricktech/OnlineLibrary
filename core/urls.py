from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import Index,DashboardView

import accounts


urlpatterns = [
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('book/', include("books.urls"), name='books'),
    path('accounts/', include('accounts.urls'), name='accounts'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
