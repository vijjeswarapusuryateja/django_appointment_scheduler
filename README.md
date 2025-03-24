# Appointment Scheduler

**Appointment Scheduler** is a generic and flexible appointment scheduling package for Django applications. It is designed to work with any model (e.g., doctor, tutor, counsellor) and provides a robust and efficient way to manage availability, slots, and appointments.

---

## Features
- **Generic and Flexible:** Works with any Django model using GenericForeignKey.
- **Advanced Slot Management:** Create, update, and delete slots dynamically.
- **Robust Booking System:** Book and cancel appointments seamlessly.
- **Efficient Slot Generation:** Automatically generate slots based on availability and slot duration.
- **Customizable Weekly Offs:** Configure off days and handle "Off" periods.
- **Conflict Resolution:** Prevents overlapping slots and handles cancellations gracefully.

---

## Installation

You can install the package using pip:

```bash
pip install django-appointment-scheduler
```

---

## 🚀 Django Appointment Scheduler - Quick Start

### Step 1: Install Dependencies
```bash
pip install Django djangorestframework
```

### Step 2: Install the Appointment Scheduler Package
```bash
pip install django-appointment-scheduler
```

### Step 3: Create a New Django Project
```bash
django-admin startproject tutor_project
cd tutor_project
```

### Step 4: Create a New App
```bash
python manage.py startapp main
```

### Step 5: Add the Package to Installed Apps
Edit your `settings.py` to include the following:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your app
    'main',
    # Appointment Scheduler Package
    'django_appointment_scheduler',
]
```

### Step 6: Define Your Models (`main/models.py`)
Create a simple model to test:
```python
from django.db import models

class Tutor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

### Step 7: Make Migrations and Migrate
```bash
python manage.py makemigrations main
python manage.py makemigrations django_appointment_scheduler
python manage.py migrate
```

### Step 8: Set Up URLs (`tutor_project/urls.py`)
Include the package URLs:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('django_appointment_scheduler.urls')),  # Include package URLs
]
```

### Step 9: Run the Server
```bash
python manage.py runserver
```

### Step 10: Create Tutor Instances via the Shell
```bash
python manage.py shell
```
```python
from main.models import Tutor

# Create some tutors
Tutor.objects.create(name="Dr. John Doe")
Tutor.objects.create(name="Dr. Jane Smith")

# Check if they are created
print(Tutor.objects.all())
```

## 📝 API Usage

### Set Availability for a Tutor
You can pass list into weekly_offs
```bash
curl -X POST http://localhost:8000/api/tutor/1/set-availability/ \
  -H "Content-Type: application/json" \
  -d '{
        "start_date": "2025-03-24",
        "end_date": "2025-03-31",
        "start_time": "10:00:00",
        "end_time": "15:00:00",
        "slot_duration": 30,
        "weekly_offs": ["Sunday"]
      }'
```
You can set the entire date range as Off by using the keyword “Off” in the weekly_offs list. This is useful when you want to mark a period as completely unavailable.
```bash
"weekly_offs": ["Off"]
```
Additionally, you can pass multiple weekdays to the weekly_offs list to mark specific days of the week as unavailable.
```bash
"weekly_offs": ["Sunday", "Friday"]
```

### Book an Appointment
```bash
curl -X POST http://localhost:8000/api/tutor/1/book-appointment/1/ \
  -H "Content-Type: application/json" \
  -d '{
        "customer_name": "Alice Johnson",
        "booked_by": "Admin"
      }'
```

### Cancel an Appointment
```bash
curl -X DELETE http://localhost:8000/api/tutor/1/cancel-appointment/1/
```

---

## 📝 Notes
For a more detailed and engaging read, check out my Medium article:
[Introducing the Django Appointment Scheduler - Your Ultimate Solution for Managing Appointments](https://medium.com/@surya.vijjeswarapu/introducing-the-django-appointment-scheduler-your-ultimate-solution-for-managing-appointments-ab2268d6f95c)

---

## 🎉 Done!
Your **Django Appointment Scheduler** is up and running! You can now manage tutor appointments seamlessly.

