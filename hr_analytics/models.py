from django.db import models
from django.utils import timezone
import datetime

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    role = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    performance_score = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # Score from 1 to 5
    
    # --- NEW FIELDS FOR ATTRITION ---
    is_active = models.BooleanField(default=True)
    termination_date = models.DateField(null=True, blank=True)

    @property
    def tenure_in_years(self):
        """Calculates employee tenure in years."""
        end_date = self.termination_date or timezone.now().date()
        return (end_date - self.hire_date).days / 365.25

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

