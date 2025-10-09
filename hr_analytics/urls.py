from django.urls import path
from .views import dashboard_view

urlpatterns = [
    # The key change is adding name='dashboard' to this line
    path('', dashboard_view, name='dashboard'),
]

