import random
from faker import Faker
from django.core.management.base import BaseCommand
from hr_analytics.models import Department, Employee
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populates the database with 12 departments and 250+ employees for a realistic look.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('System Reset: Clearing database...'))
        Employee.objects.all().delete()
        Department.objects.all().delete()
        fake = Faker()

        depts_list = [
            'Engineering', 'Product', 'Sales', 'Marketing', 'Finance', 'Legal',
            'HR', 'Operations', 'Customer Support', 'R&D', 'Quality Assurance', 'Supply Chain'
        ]
        departments = [Department.objects.create(name=name) for name in depts_list]

        employees = []
        # 1. Generate 80 Former Employees (Essential for the Attrition ML model to learn)
        for i in range(80):
            h = fake.date_between(start_date='-10y', end_date='-2y')
            t = fake.date_between(start_date=h + timedelta(days=150), end_date='-30d')
            employees.append(Employee(
                employee_id=f'HIST-{1000+i}', name=fake.name(), department=random.choice(departments),
                role='Analyst', hire_date=h, salary=random.randint(45000, 90000),
                performance_score=random.choice([1, 2, 2, 3]), is_active=False, termination_date=t
            ))

        # 2. Generate 200 Active Employees
        roles = ['Lead Engineer', 'Developer', 'Specialist', 'Manager', 'Accountant', 'Designer']
        for i in range(200):
            h = fake.date_between(start_date='-8y', end_date='today')
            employees.append(Employee(
                employee_id=f'EMP-{5000+i}', name=fake.name(), department=random.choice(departments),
                role=random.choice(roles), hire_date=h, salary=random.randint(60000, 160000),
                performance_score=random.choice([3, 3, 4, 4, 4, 5, 5]), is_active=True
            ))

        Employee.objects.bulk_create(employees)
        self.stdout.write(self.style.SUCCESS(f'Success: Created {len(employees)} records.'))