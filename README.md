# Django HR Analytics Dashboard

This is a full-stack web application built with Django that provides a comprehensive and interactive dashboard for visualizing Human Resources data. The project includes data aggregation, predictive analytics using machine learning, and a secure authentication system.


# Features

This project is packed with features designed to provide actionable insights into workforce data:

Core Dashboard & Visualizations:-

I- nteractive UI: A clean, modern, and compact dashboard interface designed for a professional user experience.

- Key Metric Cards: At-a-glance cards for critical metrics like Total Active Employees, Average Salary, Average Tenure, and Predicted Attrition Risk.

I- nteractive Filtering: A powerful dropdown menu to filter the entire dashboard by department.

- Multiple Charts: A variety of charts to visualize data from different angles:

- Employee Count by Department (Bar Chart)

- Average Salary by Department (Bar Chart)

- Performance Score Distribution (Doughnut Chart)

- Employee Tenure Distribution (Bar Chart)

- Hiring Trend Over Time (Line Chart)

- Top 5 Role Distribution (Pie Chart)

Advanced Analytics & Machine Learning:- 

- Salary Prediction: A scatter plot with a trend line that uses Linear Regression to predict salary based on employee tenure.

- Employee Attrition Prediction: A machine learning model using Logistic Regression to predict the number of current employees who are at a high risk of leaving the company.

Security & Administration:-

- User Authentication: A secure, professional login system to protect the dashboard. Only authenticated users can view the data.

- Custom Admin Panel: A customized Django admin interface that allows for easy management of employee and department data in the database.


# Tech Stack

- Backend: Python, Django

- Data Analysis & ML: Scikit-learn, Pandas, NumPy

- Frontend: HTML, Tailwind CSS, Chart.js

- Database: SQLite (default for development)


# Setup and Installation

Follow these steps to run the project locally.

1. Prerequisites

Python 3.8+

Git

2. Clone the Repository

git clone [https://github.com/your-username/django-hr-dashboard.git](https://github.com/your-username/django-hr-dashboard.git)

cd django-hr-dashboard

3. Create and Activate Virtual Environment
On Windows:

python -m venv venv

venv\Scripts\activate

On macOS/Linux:

python3 -m venv venv

source venv/bin/activate

4. Install Dependencies

pip install -r requirements.txt

5. Apply Database Migrations

This command creates the database tables based on the models.

python manage.py migrate

6. Create a Superuser

This account will be used to log in to the application and the admin panel.

python manage.py createsuperuser

(Follow the prompts to create a username and password.)

7. Populate the Database with Sample Data

This custom command fills the database with sample employees, including historical data for the attrition model.

python manage.py populate_data

8. Run the Development Server

python manage.py runserver

The application will now be running at http://127.0.0.1:8000/. You will be redirected to the login page. Use the superuser credentials you created in Step 6 to log in.

The admin panel is available at http://127.0.0.1:8000/admin/.


# New terminal run commands:-

- cd C:\hr_dashboard_project
- venv\Scripts\activate
- python manage.py runserver
