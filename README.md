Django HR Analytics Dashboard
This is a comprehensive HR Analytics Dashboard built with Django. The project provides key insights into the company's workforce, including metrics on employee demographics, salary distribution, tenure, and departmental structure. It also includes a predictive model to forecast salary based on employee tenure.


#Features

* Database Modeling: A robust database schema designed with the Django ORM to efficiently handle employee and department data.

* Data Aggregation & Visualization: Custom data aggregation logic to calculate key metrics, visualized with interactive charts using Chart.js.

* Predictive Insights: A linear regression model implemented with Scikit-learn to analyze and forecast salary trends based on employee tenure.

* Custom Admin Interface: A customized Django Admin interface for easy management of employee and department data by HR managers.
  

#Tech Stack

Backend: Python, Django

Frontend: HTML, Tailwind CSS, Chart.js

Data Analysis: Pandas, NumPy, Scikit-learn

Database: SQLite (default)


#Setup and Installation

Follow these steps to get the project running on your local machine.

1. Create a Virtual Environment
Navigate to your project's root directory and create a virtual environment.

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

2. Install Dependencies
Install all the required packages from the requirements.txt file.

 - pip install -r requirements.txt

3. Apply Migrations
Create the database tables based on the models defined in the project.

- python manage.py makemigrations hr_analytics
- python manage.py migrate

4. Create a Superuser
This account will be used to access the Django Admin interface. Follow the prompts to set a username and password.

- python manage.py createsuperuser

5. Populate with Sample Data
Run the custom management command to fill the database with 100 sample employees and 6 departments.

- python manage.py populate_data

6. Run the Development Server
Start the Django development server.

- python manage.py runserver


#Usage

HR Dashboard: Open your web browser and navigate to http://127.0.0.1:8000/

Admin Panel: Navigate to http://127.0.0.1:8000/admin/ and log in with the superuser credentials you created in Step 4.


#New terminal run commands

- cd C:\hr_dashboard_project
- venv\Scripts\activate
- python manage.py runserver

