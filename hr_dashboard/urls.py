from django.contrib import admin
from django.urls import path, include # <-- Make sure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    # --- ADD THIS LINE ---
    # This tells Django to look at the hr_analytics/urls.py file
    # for any requests to the main site (e.g., http://127.0.0.1:8000/)
    path('', include('hr_analytics.urls')),
]