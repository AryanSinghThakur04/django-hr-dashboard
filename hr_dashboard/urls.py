from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line handles login/logout and other authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    # This line includes all the URLs from your hr_analytics app (like the dashboard itself)
    path('', include('hr_analytics.urls')),
]

