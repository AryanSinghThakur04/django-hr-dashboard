Django HR Analytics & Attrition Prediction Dashboard

This project is a comprehensive HR Analytics Dashboard built with Django. It serves as a powerful tool for HR managers and data analysts to gain actionable insights into their workforce, visualize key metrics, and predict employee attrition using a machine learning model.

# Key Features:-

- Interactive Dashboard: A clean, modern, and compact user interface built with Tailwind CSS and Chart.js.

- Core HR Metrics: At-a-glance cards for critical numbers like Total Active Employees, Average Salary, and Average Tenure.

Advanced Predictive Analytics:

- Employee Attrition Risk: Utilizes a Logistic Regression model trained on historical data to predict the number of current employees at high risk of leaving the company.

- Salary Prediction: Implements a Linear Regression model to forecast salary trends based on employee tenure.

- Dynamic Filtering: An interactive dropdown menu allows for filtering the entire dashboard by department for more granular analysis.

Rich Data Visualizations: A suite of charts to provide a deep understanding of the workforce:

- Employee Count & Average Salary by Department

- Performance Score Distribution (Doughnut Chart)

- Employee Tenure Distribution (Bar Chart)

- Hiring Trends Over Time (Line Chart)

- Top 5 Role Distribution (Pie Chart)

Custom Admin Panel: A customized Django admin interface for easy data management of employees and departments.

Realistic Sample Data: A custom management command (populate_data) uses the Faker library to generate a realistic dataset, including historical attrition data for model training.

# Tech Stack:-

- Backend: Python, Django

- Data Analysis & ML: Pandas, NumPy, Scikit-learn

- Frontend: HTML, Tailwind CSS, Chart.js

- Database: SQLite (default)

# Setup and Installation:-

Follow these steps to get the project running locally.

1. Prerequisites
Python 3.8+

Git

2. Clone the Repository
git clone [https://github.com/your-username/django-hr-dashboard.git](https://github.com/your-username/django-hr-dashboard.git)
cd django-hr-dashboard

3. Create and Activate a Virtual Environment
On Windows:

python -m venv venv
venv\Scripts\activate

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt

5. Apply Database Migrations
This will create the necessary tables in your database based on the models.

python manage.py makemigrations hr_analytics
python manage.py migrate

6. Create a Superuser
This account will be used to access the Django Admin interface. Follow the prompts to create a username and password.

python manage.py createsuperuser

7. Populate the Database with Sample Data
Run the custom management command to fill the database with 150 employees (100 active, 50 inactive for model training).

python manage.py populate_data

8. Run the Development Server
python manage.py runserver


The HR Dashboard will be available at http://127.0.0.1:8000/

The Admin Panel will be available at http://127.0.0.1:8000/admin/


How the Attrition Model Works:

The predictive model is a key feature of this project.

The populate_data command generates a dataset with both active and inactive (terminated) employees. This historical data serves as the training ground.

In views.py, a LogisticRegression model from Scikit-learn is trained on this dataset. It learns the patterns associated with employees who have left, based on features like tenure, salary, and performance score.

The trained model is then used to predict the probability of attrition for all current active employees.

Employees with a predicted probability of leaving greater than 50% are flagged as "high risk," and the total count is displayed on the dashboard.

# New terminal run commands:-

- cd C:\hr_dashboard_project
- venv\Scripts\activate
- python manage.py runserver
