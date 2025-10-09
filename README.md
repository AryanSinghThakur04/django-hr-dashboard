Django HR Analytics Dashboard
This project is a comprehensive HR Analytics Dashboard built with Django. It serves as a powerful tool for HR managers and analysts to gain actionable insights into their workforce data. The dashboard provides a clean, interactive, and visually appealing interface to explore key metrics, analyze trends, and make data-driven decisions.

This project was developed to showcase skills in backend development with Django, data analysis, predictive modeling, and modern front-end design.

# Features:-

Interactive Department Filter: Dynamically filter the entire dashboard by a specific department to analyze team-level metrics.

Core HR Metrics: At-a-glance cards for Total Employees, Average Salary, and Average Tenure.

Data Visualization: A suite of interactive charts built with Chart.js, including:

- Employee Count by Department

- Average Salary by Department

- Role Distribution (Pie Chart)

- Hiring Trend Over Time (Line Chart)

- Performance Score Distribution (Doughnut Chart)

- Employee Tenure Distribution

Predictive Insights: A scatter plot with a linear regression trend line to predict future salary based on employee tenure.

Custom Admin Interface: A customized Django Admin panel for easy management of employee and department data.

Sample Data Generation: A custom management command to populate the database with 100 realistic sample employees for immediate use.


# Tech Stack:-

Backend: Django, Python

Database: SQLite (default)

Data Analysis: Pandas, NumPy

Predictive Modeling: Scikit-learn

Frontend: HTML, Tailwind CSS, JavaScript

Charting: Chart.js

# Setup and Installation:-

Follow these steps to set up and run the project locally.

1. Prerequisites
   
Python 3.8+

Git

2. Clone and Set Up the Project
# Clone the repository
git clone [https://github.com/your-username/django-hr-dashboard.git](https://github.com/your-username/django-hr-dashboard.git)

cd django-hr-dashboard

# Create and activate a virtual environment
python -m venv venv
# On Windows:
- venv\Scripts\activate
# On macOS/Linux:
- source venv/bin/activate

# Install the required dependencies
- pip install -r requirements.txt

3. Configure the Database
This project uses SQLite by default, which requires no extra setup. The migration commands will create the database file.

# Apply database migrations
- python manage.py makemigrations hr_analytics
- python manage.py migrate

4. Create a Superuser
This account is needed to access the Django Admin panel.

- python manage.py createsuperuser

Follow the prompts to create your username and password.

5. Populate with Sample Data
Run the custom management command to fill the database with 100 sample employees.

- python manage.py populate_data

# Usage:-
Running the Development Server
Once the setup is complete, you can run the local development server.

- python manage.py runserver

The application will be available at the following URLs:-

- HR Dashboard: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

# New terminal run commands:-

- cd C:\hr_dashboard_project
- venv\Scripts\activate
- python manage.py runserver
