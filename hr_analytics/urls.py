from django.urls import path
from .views import dashboard_view, employee_list_view

app_name = 'hr_analytics'

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('employees/', employee_list_view, name='employee_list'),
]