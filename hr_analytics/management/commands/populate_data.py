import random
from faker import Faker
from django.core.management.base import BaseCommand
from hr_analytics.models import Department, Employee
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populates the database with sample data, including historical attrition.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population for attrition model...'))

        # Clear existing data first
        Employee.objects.all().delete()
        Department.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing Employee and Department data.'))

        fake = Faker()

        # Create Departments
        departments_list = ['Engineering', 'Human Resources', 'Sales', 'Marketing', 'Finance', 'Product']
        departments = [Department.objects.create(name=name) for name in departments_list]
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments.'))

        employees_to_create = []
        
        # --- Create 50 former employees (historical attrition data) ---
        for i in range(50):
            hire_date = fake.date_between(start_date='-10y', end_date='-1y')
            # Ensure termination is a realistic time after hiring
            termination_date = fake.date_between(start_date=hire_date + timedelta(days=180), end_date='-30d')
            department = random.choice(departments)
            
            employee = Employee(
                employee_id=f'FORMER{1001 + i}',
                name=fake.name(),
                department=department,
                role=random.choice(['Associate', 'Specialist', 'Analyst']),
                hire_date=hire_date,
                salary=round(random.uniform(50000, 120000), 2),
                # Employees who left are more likely to have had lower performance scores
                performance_score=random.choice([1, 2, 2, 3, 3, 4]), 
                is_active=False,
                termination_date=termination_date
            )
            employees_to_create.append(employee)

        # --- Create 100 current employees ---
        for i in range(100):
            hire_date = fake.date_between(start_date='-8y', end_date='today')
            department = random.choice(departments)

            employee = Employee(
                employee_id=f'EMP{1001 + i}',
                name=fake.name(),
                department=department,
                role=random.choice(['Software Engineer', 'Account Executive', 'Marketing Lead', 'Manager']),
                hire_date=hire_date,
                salary=round(random.uniform(65000, 150000), 2),
                 # Active employees are more likely to have higher performance scores
                performance_score=random.choice([2, 3, 3, 4, 4, 5]),
                is_active=True
            )
            employees_to_create.append(employee)

        # Create all employees in one go for efficiency
        Employee.objects.bulk_create(employees_to_create)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(employees_to_create)} total employees (100 active, 50 inactive).'))

