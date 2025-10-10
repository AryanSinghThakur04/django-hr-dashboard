import json
import numpy as np
import pandas as pd
from datetime import date

from django.db import models
from django.shortcuts import render
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth

from .models import Employee, Department
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split

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

    # --- 2. Core Metrics (based on active, filtered employees) ---
    total_employees = employees_to_display.count()
    average_salary = employees_to_display.aggregate(avg_salary=Avg('salary'))['avg_salary'] or 0
    average_tenure = sum(emp.tenure_in_years for emp in employees_to_display) / total_employees if total_employees > 0 else 0

    # --- 3. Attrition Prediction Model ---
    attrition_risk_count = 0
    # We need enough historical data to train a meaningful model
    if all_employees.count() > 10 and all_employees.filter(is_active=False).count() > 1:
        # Prepare data using pandas: features (X) and target (y)
        df = pd.DataFrame.from_records(all_employees.values('tenure_in_years', 'salary', 'performance_score', 'is_active'))
        
        X = df[['tenure_in_years', 'salary', 'performance_score']]
        # Target: 1 represents attrition (is_active=False), 0 represents active
        y = df['is_active'].apply(lambda x: 0 if x else 1) 

        # Train a Logistic Regression model on the entire historical dataset
        attrition_model = LogisticRegression()
        attrition_model.fit(X, y)

        # Now, predict on the current, active employees to find who is at risk
        current_employees_df = pd.DataFrame.from_records(
            active_employees.values('tenure_in_years', 'salary', 'performance_score')
        )
        if not current_employees_df.empty:
            # Predict the probability of attrition (class 1) for each active employee
            risk_probabilities = attrition_model.predict_proba(current_employees_df)[:, 1]
            # Consider 'high risk' if the model's predicted probability of leaving is > 50%
            attrition_risk_count = int(np.sum(risk_probabilities > 0.5))


    # --- 4. Chart Data ---
    # Department charts should always show all departments for comparison, but count only active employees
    depts = Department.objects.annotate(employee_count=Count('employees', filter=models.Q(employees__is_active=True))).order_by('name')
    dept_labels = [d.name for d in depts]
    dept_employee_counts = [d.employee_count for d in depts]

    salaries_by_dept = Department.objects.annotate(avg_salary=Avg('employees__salary', filter=models.Q(employees__is_active=True))).order_by('name')
    salary_labels = [d.name for d in salaries_by_dept]
    avg_salaries = [round(float(d.avg_salary or 0), 2) for d in salaries_by_dept]
    
    # Other charts are based on the filtered set of active employees
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

    # --- 5. Salary Prediction (based on active employees) ---
    prediction_data = None
    if active_employees.count() > 1:
        tenures = np.array([e.tenure_in_years for e in active_employees]).reshape(-1, 1)
        salaries = np.array([e.salary for e in active_employees])
        model = LinearRegression().fit(tenures, salaries)
        future_tenures = np.array(range(0, 21)).reshape(-1, 1)
        predicted_salaries = model.predict(future_tenures)
        prediction_data = {
            'actual_tenures': [round(t[0], 2) for t in tenures],
            'actual_salaries': [float(s) for s in salaries],
            'predicted_salaries': [float(s) for s in predicted_salaries]
        }

    # --- 6. Prepare Context for Template ---
    context = {
        'total_employees': total_employees,
        'average_salary': average_salary,
        'average_tenure': average_tenure,
        'attrition_risk_count': attrition_risk_count, # NEW CONTEXT VARIABLE
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

