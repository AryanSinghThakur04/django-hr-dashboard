from django.contrib import admin
from .models import Department, Employee

# Register your models here to make them visible in the admin panel.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'department', 'role', 'salary', 'hire_date', 'performance_score')
    list_filter = ('department', 'performance_score', 'hire_date')
    search_fields = ('name', 'employee_id', 'role')
    ordering = ('name',)

