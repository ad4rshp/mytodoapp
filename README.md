Todo App (Django App)
This repository contains the todos Django application, designed to be integrated into an existing or new Django project. It provides a modern, responsive Todo application with vibrant gradient backgrounds and full light/dark theme support.

✨ Features
Task Management: Create, read, update, and delete (CRUD) tasks.

Task Status: Mark tasks as "In Progress," "Complete," or "On Hold."

Responsive Design: Optimized for seamless experience across desktop, tablet, and mobile devices.

Dynamic Theming: Toggle between beautiful light and dark modes with persistent preference.

Vibrant Gradients: Stylish gradient backgrounds for an engaging user interface.

User Authentication: Secure user registration and login/logout functionality.

Real-time Messages: Instant feedback for actions like saving or deleting tasks.

💻 Technologies Used
Backend:

Python

Django (Web Framework)

Django REST Framework (for API)

Frontend:

HTML5

Tailwind CSS (for styling, via CDN)

JavaScript (Vanilla JS for interactivity)

Font Awesome (for icons)

🚀 Setup Instructions
Follow these steps to integrate the todos app into your Django project and get it running on your local machine.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8+

pip (Python package installer, usually comes with Python)

Git

1. Create a New Django Project (or use an existing one)
If you don't have an existing Django project, create one:

# Create a new Django project
django-admin startproject myproject
cd myproject

2. Set up Virtual Environment and Install Dependencies
It's highly recommended to use a virtual environment:

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Django and Django REST Framework
pip install django djangorestframework

3. Integrate the todos App
Copy the todos directory:
Place the entire todos directory (from this repository) into the root of your Django project (e.g., myproject/todos/).

Add todos and rest_framework to INSTALLED_APPS:
Open myproject/myproject/settings.py and add 'todos' and 'rest_framework' to your INSTALLED_APPS list:

# myproject/myproject/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Add this line
    'todos',          # Add this line
]

Include todos URLs:
Open myproject/myproject/urls.py and include the todos app's URLs:

# myproject/myproject/urls.py
from django.contrib import admin
from django.urls import path, include # Ensure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todos.urls')), # Add this line to include todos app URLs
]

4. Database Migrations and Running the Server
From your main project directory (myproject/):

# Apply database migrations for all apps, including 'todos'
python manage.py makemigrations
python manage.py migrate

# Create a superuser (optional, for admin panel access)
python manage.py createsuperuser

# Run the Django development server
python manage.py runserver

The backend server should now be running at http://127.0.0.1:8000/.

5. Access the Application
Open your web browser and navigate to:

Sign Up: http://127.0.0.1:8000/signup/

Login: http://127.0.0.1:8000/login/

Todo App: http://127.0.0.1:8000/ (after logging in)

💡 Usage
Sign Up / Login: Create a new account or log in with existing credentials.

Add Task: Click the "Add New Task" button, fill in the description and due date, then save.

Edit Task: Click the pencil icon on a task card to open the edit modal.

Change Status: Click the refresh icon on a task card to cycle its status (In Progress -> Complete -> On Hold).

Delete Task: In the edit modal, click the "Delete Task" button.

Filter Tasks: Use the sidebar menu to filter tasks by status (All, In Progress, Complete, On Hold).

Toggle Theme: Use the moon/sun icon in the navigation bar to switch between light and dark themes.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or find a bug, please open an issue or submit a pull request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
