import random
from faker import Faker
from django.core.management.base import BaseCommand
from hr_analytics.models import Department, Employee
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populates the database with expanded sample data for a more detailed dashboard.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting expanded database population...'))

        # Clear existing data first
        Employee.objects.all().delete()
        Department.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing Employee and Department data.'))

        fake = Faker()

        # Expanded Departments List (12 Departments)
        departments_list = [
            'Engineering', 'Human Resources', 'Sales', 'Marketing', 
            'Finance', 'Product', 'Legal', 'Customer Support', 
            'Operations', 'R&D', 'Quality Assurance', 'Supply Chain'
        ]
        departments = [Department.objects.create(name=name) for name in departments_list]
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments.'))

        employees_to_create = []
        
        # --- Create 80 former employees (Improved historical attrition data) ---
        for i in range(80):
            hire_date = fake.date_between(start_date='-12y', end_date='-2y')
            # Termination date is a realistic time after hiring
            termination_date = fake.date_between(start_date=hire_date + timedelta(days=120), end_date='-60d')
            department = random.choice(departments)
            
            employee = Employee(
                employee_id=f'FORMER{2000 + i}',
                name=fake.name(),
                department=department,
                role=random.choice(['Associate', 'Specialist', 'Analyst', 'Junior Dev', 'Intern', 'Coordinator']),
                hire_date=hire_date,
                salary=round(random.uniform(45000, 110000), 2),
                # Lower performance scores often correlate with attrition
                performance_score=random.choice([1, 1, 2, 2, 3, 3, 4]), 
                is_active=False,
                termination_date=termination_date
            )
            employees_to_create.append(employee)

        # --- Create 200 current employees ---
        roles = [
            'Software Engineer', 'Senior Developer', 'Data Scientist', 'HR Specialist', 
            'Account Executive', 'Marketing Lead', 'Finance Analyst', 'Product Manager', 
            'UX Designer', 'Operations Coordinator', 'Legal Counsel', 'Support Lead',
            'QA Engineer', 'Scrum Master', 'Sales Director', 'Project Manager'
        ]

        for i in range(200):
            hire_date = fake.date_between(start_date='-10y', end_date='today')
            department = random.choice(departments)

            employee = Employee(
                employee_id=f'EMP{5000 + i}',
                name=fake.name(),
                department=department,
                role=random.choice(roles),
                hire_date=hire_date,
                salary=round(random.uniform(60000, 165000), 2),
                # Active employees generally have a higher performance distribution
                performance_score=random.choice([2, 3, 3, 4, 4, 4, 5, 5]),
                is_active=True
            )
            employees_to_create.append(employee)

        # Create all employees in one go for efficiency
        Employee.objects.bulk_create(employees_to_create)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {len(employees_to_create)} total employees '
            f'(200 active, 80 inactive) across 12 departments.'
<<<<<<< HEAD
        ))
=======
        ))
>>>>>>> 30e69e80bba0a15c82ff97866af95ee070d12539
