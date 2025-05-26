python -m django startproject maintenance_manager .
python -m django startapp maintenancepython -m django startproject maintenance_manager .
python -m django startapp maintenancepython -m django startproject maintenance_manager .
python -m django startapp maintenance# Machine Maintenance Management System

A Django-based web application for managing machine maintenance operations.

## Features

- User Management (Admin and Technician roles)
- Machine Management (Add/Edit machines)
- Fault Logging System
- Maintenance Tracking
- Excel Export of Fault History
- Dashboard with Statistics

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `maintenance/`: Main app containing models, views, and templates
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and other static files
- `media/`: User-uploaded files
