import json
import numpy as np
import pandas as pd
from datetime import date

from django.shortcuts import render
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth

from .models import Employee, Department
from sklearn.linear_model import LinearRegression

def dashboard_view(request):
    """
    Main view for the HR analytics dashboard.
    Handles data aggregation, prediction, and filtering.
    """
    
    # --- 1. Department Filtering ---
    selected_department_id = request.GET.get('department')
    
    employees = Employee.objects.all()
    if selected_department_id:
        employees = employees.filter(department_id=selected_department_id)

    # --- 2. Core Metrics ---
    total_employees = employees.count()
    average_salary = employees.aggregate(avg_salary=Avg('salary'))['avg_salary'] or 0
    
    total_tenure = sum(emp.tenure_in_years for emp in employees)
    average_tenure = (total_tenure / total_employees) if total_employees > 0 else 0

    # --- 3. Existing Chart Data ---
    depts = Department.objects.annotate(employee_count=Count('employees')).order_by('name')
    dept_labels = [d.name for d in depts]
    dept_employee_counts = [d.employee_count for d in depts]

    salaries_by_dept = Department.objects.annotate(avg_salary=Avg('employees__salary')).order_by('name')
    salary_labels = [d.name for d in salaries_by_dept]
    avg_salaries = [round(float(d.avg_salary or 0), 2) for d in salaries_by_dept]

    performance_counts = employees.values('performance_score').annotate(count=Count('id')).order_by('performance_score')
    performance_labels = [f"Score {item['performance_score']}" for item in performance_counts]
    performance_data = [item['count'] for item in performance_counts]

    tenure_bins = {"< 1 Year": 0, "1-3 Years": 0, "3-5 Years": 0, "5-10 Years": 0, "10+ Years": 0}
    for emp in employees:
        tenure = emp.tenure_in_years
        if tenure < 1: tenure_bins["< 1 Year"] += 1
        elif 1 <= tenure < 3: tenure_bins["1-3 Years"] += 1
        elif 3 <= tenure < 5: tenure_bins["3-5 Years"] += 1
        elif 5 <= tenure < 10: tenure_bins["5-10 Years"] += 1
        else: tenure_bins["10+ Years"] += 1
    tenure_labels = list(tenure_bins.keys())
    tenure_data = list(tenure_bins.values())

    # --- 4. NEW CHARTS ---
    # Hiring Trend Over Time
    hiring_trend = employees.annotate(month=TruncMonth('hire_date')).values('month').annotate(count=Count('id')).order_by('month')
    hiring_trend_labels = [h['month'].strftime('%b %Y') for h in hiring_trend]
    hiring_trend_data = [h['count'] for h in hiring_trend]

    # Role Distribution
    role_distribution = employees.values('role').annotate(count=Count('id')).order_by('-count')
    top_roles = role_distribution[:5]
    other_count = sum(item['count'] for item in role_distribution[5:])
    role_labels = [item['role'] for item in top_roles]
    role_data = [item['count'] for item in top_roles]
    if other_count > 0:
        role_labels.append('Other')
        role_data.append(other_count)

    # --- 5. Predictive Analysis ---
    all_employees_for_pred = Employee.objects.all()
    prediction_data = None
    if all_employees_for_pred.count() > 1:
        tenures = np.array([e.tenure_in_years for e in all_employees_for_pred]).reshape(-1, 1)
        salaries = np.array([e.salary for e in all_employees_for_pred])
        model = LinearRegression().fit(tenures, salaries)
        future_tenures = np.array(range(0, 21)).reshape(-1, 1)
        predicted_salaries = model.predict(future_tenures)
        prediction_data = {
            'actual_tenures': [round(t[0], 2) for t in tenures],
            'actual_salaries': [float(s) for s in salaries],
            'predicted_salaries': [float(s) for s in predicted_salaries]
        }

    # --- 6. Prepare Context ---
    context = {
        'total_employees': total_employees,
        'average_salary': average_salary,
        'average_tenure': average_tenure,
        'dept_labels': dept_labels,
        'dept_employee_counts': dept_employee_counts,
        'salary_labels': salary_labels,
        'avg_salaries': avg_salaries,
        'prediction_data_json': json.dumps(prediction_data) if prediction_data else "null",
        'performance_labels': performance_labels,
        'performance_data': performance_data,
        'tenure_labels': tenure_labels,
        'tenure_data': tenure_data,
        'departments': Department.objects.all(),
        'selected_department_id': int(selected_department_id) if selected_department_id else None,
        # New context for new charts
        'hiring_trend_labels': hiring_trend_labels,
        'hiring_trend_data': hiring_trend_data,
        'role_labels': role_labels,
        'role_data': role_data,
    }

    return render(request, 'hr_analytics/dashboard.html', context)

