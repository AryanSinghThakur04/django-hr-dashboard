from django.urls import path
from .views import dashboard_view

# app_name helps Django differentiate URLs between apps, which is good practice
app_name = 'hr_analytics'

urlpatterns = [
    # This line maps the root URL of the app ('') to your dashboard view
    # and gives it a unique name for use in templates.
    path('', dashboard_view, name='dashboard'),
]

