import json
import numpy as np
import pandas as pd
from datetime import date

from django.db import models
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

from .models import Employee, Department
from sklearn.linear_model import LinearRegression, LogisticRegression

@login_required
def dashboard_view(request):
    """
    Main dashboard view. Handles data aggregation, filtering, 
    and predictive machine learning models.
    """
    selected_department_id = request.GET.get('department')
    
    all_employees = Employee.objects.all()
    active_employees = all_employees.filter(is_active=True)
    
    # 1. Apply Filtering
    employees_to_display = active_employees
    if selected_department_id and selected_department_id.isdigit():
        employees_to_display = active_employees.filter(department_id=selected_department_id)

    # 2. Core Metrics
    total_employees = employees_to_display.count()
    average_salary = employees_to_display.aggregate(avg_salary=Avg('salary'))['avg_salary'] or 0
    average_tenure = sum(emp.tenure_in_years for emp in employees_to_display) / total_employees if total_employees > 0 else 0

    # 3. Attrition Prediction (Logistic Regression)
    attrition_risk_count = 0
    if all_employees.count() > 10 and all_employees.filter(is_active=False).count() > 1:
        training_data = [
            {'tenure_in_years': emp.tenure_in_years, 'salary': float(emp.salary), 'performance_score': emp.performance_score, 'is_active': 1 if emp.is_active else 0}
            for emp in all_employees
        ]
        df = pd.DataFrame(training_data)
        X = df[['tenure_in_years', 'salary', 'performance_score']]
        y = df['is_active'].apply(lambda x: 0 if x == 1 else 1) 
        attrition_model = LogisticRegression(max_iter=1000).fit(X, y)
        current_data = [{'tenure_in_years': e.tenure_in_years, 'salary': float(e.salary), 'performance_score': e.performance_score} for e in employees_to_display]
        if current_data:
            current_df = pd.DataFrame(current_data)
            probs = attrition_model.predict_proba(current_df)[:, 1]
            attrition_risk_count = int(np.sum(probs > 0.5))

    # 4. Chart Data Preparation
    dept_qs = Department.objects.all().order_by('name')
    if selected_department_id and selected_department_id.isdigit():
        dept_qs = dept_qs.filter(id=selected_department_id)

    depts = dept_qs.annotate(emp_count=Count('employees', filter=Q(employees__is_active=True)))
    dept_labels = [d.name for d in depts]
    dept_ids = [d.id for d in depts]
    dept_employee_counts = [d.emp_count for d in depts]

    salaries_by_dept = dept_qs.annotate(avg_sal=Avg('employees__salary', filter=Q(employees__is_active=True)))
    avg_salaries = [round(float(d.avg_sal or 0), 2) for d in salaries_by_dept]
    
    performance_counts = employees_to_display.values('performance_score').annotate(count=Count('id')).order_by('performance_score')
    performance_labels = [f"Score {item['performance_score']}" for item in performance_counts]
    performance_data = [item['count'] for item in performance_counts]
    
    tenure_bins = {"< 1 Year": 0, "1-3 Years": 0, "3-5 Years": 0, "5-10 Years": 0, "10+ Years": 0}
    for emp in employees_to_display:
        t = emp.tenure_in_years
        if t < 1: tenure_bins["< 1 Year"] += 1
        elif 1 <= t < 3: tenure_bins["1-3 Years"] += 1
        elif 3 <= t < 5: tenure_bins["3-5 Years"] += 1
        elif 5 <= t < 10: tenure_bins["5-10 Years"] += 1
        else: tenure_bins["10+ Years"] += 1

    hiring_trend = employees_to_display.annotate(month=TruncMonth('hire_date')).values('month').annotate(count=Count('id')).order_by('month')
    hiring_labels = [d['month'].strftime('%b %Y') for d in hiring_trend]
    hiring_data = [d['count'] for d in hiring_trend]

    # Roles Data (Added back to logic)
    role_counts = employees_to_display.values('role').annotate(count=Count('id')).order_by('-count')[:5]
    role_labels = [r['role'] for r in role_counts]
    role_data = [r['count'] for r in role_counts]

    # 5. Salary Prediction (Linear Regression)
    prediction_data = None
    if employees_to_display.count() > 1:
        t_arr = np.array([e.tenure_in_years for e in employees_to_display]).reshape(-1, 1)
        s_arr = np.array([float(e.salary) for e in employees_to_display])
        model = LinearRegression().fit(t_arr, s_arr)
        pred = model.predict(np.array(range(0, 21)).reshape(-1, 1))
        prediction_data = {'actual_tenures': [round(t[0], 2) for t in t_arr], 'actual_salaries': list(s_arr), 'predicted_salaries': [float(p) for p in pred]}

    context = {
        'total_employees': total_employees,
        'average_salary': average_salary,
        'average_tenure': average_tenure,
        'attrition_risk_count': attrition_risk_count,
        'dept_labels': dept_labels,
        'dept_ids': dept_ids,
        'dept_employee_counts': dept_employee_counts,
        'salary_labels': dept_labels,
        'avg_salaries': avg_salaries,
        'performance_labels': performance_labels,
        'performance_data': performance_data,
        'tenure_labels': list(tenure_bins.keys()),
        'tenure_data': list(tenure_bins.values()),
        'hiring_trend_labels': hiring_labels,
        'hiring_trend_data': hiring_data,
        'role_labels': role_labels, # Added to context
        'role_data': role_data,     # Added to context
        'prediction_data': prediction_data,
        'departments': Department.objects.all().order_by('name'),
        'selected_department_id': int(selected_department_id) if (selected_department_id and selected_department_id.isdigit()) else None,
    }

    return render(request, 'hr_analytics/dashboard.html', context)

@login_required
def employee_list_view(request):
    dept_id = request.GET.get('department')
    employees = Employee.objects.filter(is_active=True).order_by('name')
    title = "All Employees"
    if dept_id and dept_id.isdigit():
        dept = get_object_or_404(Department, id=dept_id)
        employees = employees.filter(department=dept)
        title = f"Employees: {dept.name}"
    return render(request, 'hr_analytics/employee_list.html', {'employees': employees, 'title': title})