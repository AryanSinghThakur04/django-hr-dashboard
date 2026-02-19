import random
from faker import Faker
from django.core.management.base import BaseCommand
from hr_analytics.models import Department, Employee
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populates the database. Fixes the SyntaxError (unmatched parenthesis).'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting population...'))
        Employee.objects.all().delete()
        Department.objects.all().delete()
        fake = Faker()

        departments_list = ['Engineering', 'HR', 'Sales', 'Marketing', 'Finance', 'Legal']
        departments = [Department.objects.create(name=name) for name in departments_list]

        employees_to_create = []
        
        # Inactive Employees
        for i in range(50):
            hire_date = fake.date_between(start_date='-10y', end_date='-2y')
            term_date = fake.date_between(start_date=hire_date + timedelta(days=100), end_date='-30d')
            employees_to_create.append(Employee(
                employee_id=f'F{100+i}', name=fake.name(), department=random.choice(departments),
                role='Analyst', hire_date=hire_date, salary=random.randint(50000, 90000),
                performance_score=random.choice([1, 2, 3]), is_active=False, termination_date=term_date
            ))

        # Active Employees
        for i in range(150):
            hire_date = fake.date_between(start_date='-8y', end_date='today')
            employees_to_create.append(Employee(
                employee_id=f'E{500+i}', name=fake.name(), department=random.choice(departments),
                role=random.choice(['Manager', 'Developer', 'Designer']), hire_date=hire_date,
                salary=random.randint(60000, 150000), performance_score=random.choice([3, 4, 5]), is_active=True
            ))

        Employee.objects.bulk_create(employees_to_create)
        self.stdout.write(self.style.SUCCESS(f'Created {len(employees_to_create)} employees.'))