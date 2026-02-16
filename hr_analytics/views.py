import json
import numpy as np
import pandas as pd
from datetime import date

from django.db import models
from django.shortcuts import render
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

from .models import Employee, Department
from sklearn.linear_model import LinearRegression, LogisticRegression

@login_required
def dashboard_view(request):
    """
    Main view for the HR analytics dashboard.
    Handles data aggregation, prediction, and filtering.
    """
    
    # --- 1. Department Filtering ---
    selected_department_id = request.GET.get('department')
    
    all_employees = Employee.objects.all()
    active_employees = all_employees.filter(is_active=True)
    
    # This is the dataset that will be shown on the dashboard (filtered or not)
    employees_to_display = active_employees
    if selected_department_id:
        employees_to_display = active_employees.filter(department_id=selected_department_id)

    # --- 2. Core Metrics ---
    total_employees = employees_to_display.count()
    average_salary = employees_to_display.aggregate(avg_salary=Avg('salary'))['avg_salary'] or 0
    average_tenure = sum(emp.tenure_in_years for emp in employees_to_display) / total_employees if total_employees > 0 else 0

    # --- 3. Attrition Prediction Model ---
    attrition_risk_count = 0
    # Check if we have enough data to train (need both active and inactive examples)
    if all_employees.count() > 10 and all_employees.filter(is_active=False).count() > 1:
        # FIX: We build the list manually instead of using .values() because tenure_in_years is a property
        training_data = [
            {
                'tenure_in_years': emp.tenure_in_years,
                'salary': float(emp.salary),
                'performance_score': emp.performance_score,
                'is_active': 1 if emp.is_active else 0
            }
            for emp in all_employees
        ]
        
        df = pd.DataFrame(training_data)
        X = df[['tenure_in_years', 'salary', 'performance_score']]
        y = df['is_active'].apply(lambda x: 0 if x == 1 else 1) # 1 for attrition risk

        attrition_model = LogisticRegression(max_iter=1000)
        attrition_model.fit(X, y)

        # Predict for current active employees
        current_data = [
            {
                'tenure_in_years': emp.tenure_in_years,
                'salary': float(emp.salary),
                'performance_score': emp.performance_score
            }
            for emp in active_employees
        ]
        
        if current_data:
            current_employees_df = pd.DataFrame(current_data)
            risk_probabilities = attrition_model.predict_proba(current_employees_df)[:, 1]
            attrition_risk_count = int(np.sum(risk_probabilities > 0.5))


    # --- 4. Chart Data ---
    depts = Department.objects.annotate(
        employee_count=Count('employees', filter=Q(employees__is_active=True))
    ).order_by('name')
    dept_labels = [d.name for d in depts]
    dept_employee_counts = [d.employee_count for d in depts]

    salaries_by_dept = Department.objects.annotate(
        avg_salary=Avg('employees__salary', filter=Q(employees__is_active=True))
    ).order_by('name')
    salary_labels = [d.name for d in salaries_by_dept]
    avg_salaries = [round(float(d.avg_salary or 0), 2) for d in salaries_by_dept]
    
    performance_counts = employees_to_display.values('performance_score').annotate(count=Count('id')).order_by('performance_score')
    performance_labels = [f"Score {item['performance_score']}" for item in performance_counts]
    performance_data = [item['count'] for item in performance_counts]
    
    tenure_bins = {"< 1 Year": 0, "1-3 Years": 0, "3-5 Years": 0, "5-10 Years": 0, "10+ Years": 0}
    for emp in employees_to_display:
        tenure = emp.tenure_in_years
        if tenure < 1: tenure_bins["< 1 Year"] += 1
        elif 1 <= tenure < 3: tenure_bins["1-3 Years"] += 1
        elif 3 <= tenure < 5: tenure_bins["3-5 Years"] += 1
        elif 5 <= tenure < 10: tenure_bins["5-10 Years"] += 1
        else: tenure_bins["10+ Years"] += 1
    tenure_labels = list(tenure_bins.keys())
    tenure_data = list(tenure_bins.values())

    hiring_trend = active_employees.annotate(month=TruncMonth('hire_date')).values('month').annotate(count=Count('id')).order_by('month')
    hiring_trend_labels = [d['month'].strftime('%b %Y') for d in hiring_trend]
    hiring_trend_data = [d['count'] for d in hiring_trend]

    role_counts = employees_to_display.values('role').annotate(count=Count('id')).order_by('-count')[:5]
    role_labels = [r['role'] for r in role_counts]
    role_data = [r['count'] for r in role_counts]

    # --- 5. Salary Prediction ---
    prediction_data = None
    if active_employees.count() > 1:
        # Using dot notation on objects here is safe
        tenures = np.array([e.tenure_in_years for e in active_employees]).reshape(-1, 1)
        salaries = np.array([float(e.salary) for e in active_employees])
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
        'attrition_risk_count': attrition_risk_count,
        'dept_labels': dept_labels,
        'dept_employee_counts': dept_employee_counts,
        'salary_labels': salary_labels,
        'avg_salaries': avg_salaries,
        'prediction_data': prediction_data,
        'performance_labels': performance_labels,
        'performance_data': performance_data,
        'tenure_labels': tenure_labels,
        'tenure_data': tenure_data,
        'hiring_trend_labels': hiring_trend_labels,
        'hiring_trend_data': hiring_trend_data,
        'role_labels': role_labels,
        'role_data': role_data,
        'departments': Department.objects.all(),
        'selected_department_id': int(selected_department_id) if selected_department_id else None,
    }

    return render(request, 'hr_analytics/dashboard.html', context)
