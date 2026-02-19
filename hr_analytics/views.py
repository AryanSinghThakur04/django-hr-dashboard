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
    Main Analytics Hub. 
    Processes workforce data and generates ML-based predictions.
    """
    selected_department_id = request.GET.get('department')
    all_employees = Employee.objects.all()
    active_employees = all_employees.filter(is_active=True)
    
    # 1. Systematized Filtering
    employees_to_display = active_employees
    if selected_department_id and selected_department_id.isdigit():
        employees_to_display = active_employees.filter(department_id=selected_department_id)

    # 2. Advanced Metrics (Python-level calculation to avoid FieldError)
    total_employees = employees_to_display.count()
    average_salary = employees_to_display.aggregate(avg_salary=Avg('salary'))['avg_salary'] or 0
    average_tenure = sum(emp.tenure_in_years for emp in employees_to_display) / total_employees if total_employees > 0 else 0

    # 3. Predictive Engine (Logistic Regression for Attrition)
    attrition_risk_count = 0
    if all_employees.count() > 10 and all_employees.filter(is_active=False).count() > 1:
        # Train on full historical dataset
        train_data = [{'t': e.tenure_in_years, 's': float(e.salary), 'p': e.performance_score, 'a': 1 if e.is_active else 0} for e in all_employees]
        df = pd.DataFrame(train_data)
        X_train = df[['t', 's', 'p']]
        y_train = df['a'].apply(lambda x: 0 if x == 1 else 1) # 1 = Risk
        
        clf = LogisticRegression(max_iter=1000).fit(X_train, y_train)
        
        # Predict on current filtered set
        curr_data = [{'t': e.tenure_in_years, 's': float(e.salary), 'p': e.performance_score} for e in employees_to_display]
        if curr_data:
            probs = clf.predict_proba(pd.DataFrame(curr_data))[:, 1]
            attrition_risk_count = int(np.sum(probs > 0.5))

    # 4. Systematic Charting Data
    dept_qs = Department.objects.all().order_by('name')
    if selected_department_id and selected_department_id.isdigit():
        dept_qs = dept_qs.filter(id=selected_department_id)

    # Headcounts & Salaries
    depts = dept_qs.annotate(count=Count('employees', filter=Q(employees__is_active=True)))
    dept_labels = [d.name for d in depts]
    dept_ids = [d.id for d in depts]
    dept_counts = [d.count for d in depts]
    
    sal_qs = dept_qs.annotate(avg=Avg('employees__salary', filter=Q(employees__is_active=True)))
    avg_salaries = [round(float(d.avg or 0), 2) for d in sal_qs]
    
    # Performance Distribution
    perf_counts = employees_to_display.values('performance_score').annotate(c=Count('id')).order_by('performance_score')
    perf_labels = [f"Score {p['performance_score']}" for p in perf_counts]
    perf_data = [p['c'] for p in perf_counts]
    
    # Tenure Cohorts
    tenure_bins = {"<1 yr": 0, "1-3 yrs": 0, "3-5 yrs": 0, "5-10 yrs": 0, "10+ yrs": 0}
    for emp in employees_to_display:
        t = emp.tenure_in_years
        if t < 1: tenure_bins["<1 yr"] += 1
        elif 1 <= t < 3: tenure_bins["1-3 yrs"] += 1
        elif 3 <= t < 5: tenure_bins["3-5 yrs"] += 1
        elif 5 <= t < 10: tenure_bins["5-10 yrs"] += 1
        else: tenure_bins["10+ yrs"] += 1

    # Trends & Roles
    hiring = employees_to_display.annotate(m=TruncMonth('hire_date')).values('m').annotate(c=Count('id')).order_by('m')
    hire_labels = [h['m'].strftime('%b %Y') for h in hiring]
    hire_data = [h['c'] for h in hiring]

    roles = employees_to_display.values('role').annotate(c=Count('id')).order_by('-c')[:5]
    role_labels = [r['role'] for r in roles]
    role_data = [r['c'] for r in roles]

    # 5. Salary Projection (Linear Regression)
    prediction_data = None
    if employees_to_display.count() > 1:
        X_sal = np.array([e.tenure_in_years for e in employees_to_display]).reshape(-1, 1)
        y_sal = np.array([float(e.salary) for e in employees_to_display])
        reg = LinearRegression().fit(X_sal, y_sal)
        prediction_data = {
            'actual_x': [round(x[0], 1) for x in X_sal],
            'actual_y': list(y_sal),
            'pred_y': [float(p) for p in reg.predict(np.array(range(0, 21)).reshape(-1, 1))]
        }

    context = {
        'total_employees': total_employees, 'average_salary': average_salary, 'average_tenure': average_tenure,
        'attrition_risk': attrition_risk_count, 'dept_labels': dept_labels, 'dept_ids': dept_ids,
        'dept_counts': dept_counts, 'avg_salaries': avg_salaries, 'perf_labels': perf_labels, 
        'perf_data': perf_data, 'tenure_labels': list(tenure_bins.keys()), 'tenure_data': list(tenure_bins.values()),
        'hire_labels': hire_labels, 'hire_data': hire_data, 'role_labels': role_labels, 'role_data': role_data,
        'prediction_data': prediction_data, 'departments': Department.objects.all().order_by('name'),
        'selected_dept': int(selected_department_id) if (selected_department_id and selected_department_id.isdigit()) else None,
    }
    return render(request, 'hr_analytics/dashboard.html', context)

@login_required
def employee_list_view(request):
    """
    Team Directory with Drill-down capability.
    """
    dept_id = request.GET.get('department')
    employees = Employee.objects.filter(is_active=True).order_by('name')
    title = "Global Team Directory"
    if dept_id and dept_id.isdigit():
        dept = get_object_or_404(Department, id=dept_id)
        employees = employees.filter(department=dept)
        title = f"{dept.name} Division"
    return render(request, 'hr_analytics/employee_list.html', {'employees': employees, 'title': title})