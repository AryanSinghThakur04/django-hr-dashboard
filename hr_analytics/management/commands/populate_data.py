import random
from faker import Faker
from django.core.management.base import BaseCommand
from hr_analytics.models import Department, Employee
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the database with sample data for the HR analytics dashboard.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Clean up old data
        Employee.objects.all().delete()
        Department.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing Employee and Department data.'))

        fake = Faker()

        # Create Departments
        departments_list = ['Engineering', 'Human Resources', 'Sales', 'Marketing', 'Finance', 'Product']
        departments = []
        for dept_name in departments_list:
            dept, created = Department.objects.get_or_create(name=dept_name)
            departments.append(dept)
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments.'))

        # Create Employees
        employees = []
        for i in range(100):
            hire_date = fake.date_between(start_date='-10y', end_date='today')
            department = random.choice(departments)

            if department.name == 'Engineering':
                role = random.choice(['Software Engineer', 'DevOps Engineer', 'QA Tester', 'Engineering Manager'])
                base_salary = random.uniform(80000, 150000)
            elif department.name == 'Sales':
                role = random.choice(['Sales Development Rep', 'Account Executive', 'Sales Manager'])
                base_salary = random.uniform(60000, 110000)
            elif department.name == 'Marketing':
                role = random.choice(['Content Creator', 'SEO Specialist', 'Marketing Lead'])
                base_salary = random.uniform(55000, 95000)
            else:
                role = 'Associate'
                base_salary = random.uniform(50000, 80000)

            employee = Employee(
                employee_id=f'EMP{1001 + i}',
                name=fake.name(),
                department=department,
                role=role,
                hire_date=hire_date,
                salary=round(base_salary, 2),
                performance_score=random.randint(1, 5)
            )
            employees.append(employee)

        Employee.objects.bulk_create(employees)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(employees)} employees.'))
        self.stdout.write(self.style.SUCCESS('Database population complete!'))