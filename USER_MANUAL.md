# Trinity University Hostel Management System - User Manual

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [User Roles & Features](#user-roles--features)
7. [Student Guide](#student-guide)
8. [Administrator Guide](#administrator-guide)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)

---

## Overview

Trinity University Hostel Management System is a comprehensive web-based platform designed to streamline hostel accommodation requests and allocations for students and administrative staff.

### Key Features
- **Student Portal**: Submit hostel requests with preferred hostel and room selection
- **Admin Dashboard**: Manage requests, approve/reject applications, and track allocations
- **Matric Number Authentication**: Students login using their matric number for easy access
- **Real-time Status Tracking**: Track request status from submission to allocation
- **Gender-Based Filtering**: Automatic filtering of hostels based on student gender
- **Room Occupancy Management**: Track available rooms and capacity utilization
- **Responsive Design**: Access from desktop, tablet, or mobile devices

---

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 500MB minimum
- **Browser**: Chrome, Firefox, Safari, or Edge (modern versions)

### Recommended Requirements
- **Python**: 3.10+
- **RAM**: 4GB or more
- **Storage**: 1GB or more
- **Bandwidth**: Stable internet connection

---

## Installation Guide

### Step 1: Clone/Download the Project

```bash
# Navigate to your desired directory
cd Documents
# Download or clone the project
git clone <repository-url> hostelredo
cd hostelredo
```

### Step 2: Create a Virtual Environment

#### On Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

#### On Windows (Command Prompt):
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat
```

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# With virtual environment activated
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Open `.env` file in the project root
2. Update the following values if needed:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

### Step 5: Run Database Migrations

```bash
# Apply all migrations
python manage.py migrate

# Create superuser account (for admin access)
python manage.py createsuperuser

# Load initial data (hostels, students, rooms)
python manage.py loaddata fixtures/initial_data.json
```

### Step 6: Create a Superuser

When prompted during `createsuperuser`:
```
Username: admin
Email: admin@trinity.edu
Password: (create a strong password)
```

---

## Configuration

### Environment Variables (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode (True/False) | True |
| `SECRET_KEY` | Django secret key | Generated |
| `ALLOWED_HOSTS` | Allowed host domains | localhost,127.0.0.1 |
| `DB_ENGINE` | Database engine | sqlite3 |
| `DB_NAME` | Database name | db.sqlite3 |
| `ENABLE_MATRIC_LOGIN` | Enable matric number login | True |

### Database Configuration

**Default (SQLite)** - suitable for development:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**For PostgreSQL** (production):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hostel_management',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Running the Application

### Development Server

```bash
# Make sure virtual environment is activated
python manage.py runserver

# The application will be available at:
# http://localhost:8000/
# http://127.0.0.1:8000/
```

### Accessing the Application

1. **Home Page**: http://localhost:8000/
2. **Login**: http://localhost:8000/accounts/login/
3. **Admin Panel**: http://localhost:8000/admin/

### Stopping the Server

Press `Ctrl + C` in your terminal

---

## User Roles & Features

### Student Role

**Permissions:**
- View hostel information
- Submit hostel requests
- Track request status
- View room allocations
- Update profile information

**Features:**
- Dashboard with personal information
- Request status tracking (Pending → Approved → Allocated)
- Real-time room availability
- Gender-appropriate hostel filtering

### Administrator Role

**Permissions:**
- Manage all student requests
- Approve/reject hostel requests
- View allocation overview
- Generate occupancy reports
- Manage hostel and room information

**Features:**
- Request management dashboard
- Batch approval/rejection
- Allocation tracking
- Occupancy statistics
- Student profile management

---

## Student Guide

### Logging In

#### Using Matric Number (Recommended)
1. Go to http://localhost:8000/accounts/login/
2. Enter your **Matric Number** (e.g., STU001)
3. Enter your **Password**
4. Click **Login**

#### Using Username (Alternative)
1. Enter your **Username**
2. Enter your **Password**
3. Click **Login**

### Submitting a Hostel Request

1. **Go to Dashboard**
   - After login, click "My Dashboard"
   - Or navigate to http://localhost:8000/student/dashboard/

2. **Submit Request**
   - Click "Request Hostel" button
   - Fill in the request form:
     - **Preferred Hostel**: Select from gender-filtered list
     - **Room Capacity**: Choose preferred room size (2, 4, 6 beds)
     - **Preferred Room** (optional): Select specific room if available
   - Click **Submit Request**

3. **Track Status**
   - View status on dashboard:
     - **Pending**: Awaiting admin review
     - **Approved**: Request approved, awaiting allocation
     - **Allocated**: Room assigned, allocation details shown

### Viewing Your Allocation

1. After approval, your allocated room details appear on dashboard
2. Information includes:
   - Room number and location
   - Floor and building
   - Roommate names (if assigned)
   - Room amenities

### Updating Profile

1. Click **My Profile**
2. Update information as needed
3. Click **Save Changes**

### Logging Out

- Click your username dropdown (top right)
- Click **Logout**
- You'll be redirected to home page

---

## Administrator Guide

### Accessing Admin Panel

1. Navigate to http://localhost:8000/admin/
2. Log in with superuser credentials
3. You'll see the admin dashboard

### Managing Hostel Requests

#### View Requests
1. Click **Admin Requests** on dashboard
2. View all pending student requests
3. Filter by status, hostel, or student name

#### Approve Request
1. Open request details
2. Review student information
3. Click **Approve**
4. System automatically allocates best available room

#### Reject Request
1. Open request details
2. Enter rejection reason (optional)
3. Click **Reject**
4. Student receives notification

### Viewing Allocations

1. Click **View Allocations**
2. See all active room allocations
3. View occupancy rates per hostel
4. Check available capacity

### Managing Hostels

#### Add New Hostel
1. Go to Admin → Hostels
2. Click **Add Hostel**
3. Enter details:
   - Name
   - Gender (Male/Female)
   - Description
4. Click **Save**

#### Add Floors & Rooms
1. Select hostel
2. Add floors with floor number
3. Add rooms to each floor with details:
   - Room number
   - Capacity (beds)
   - Features

### Student Management

#### View Students
1. Go to Admin → Students
2. View all registered students
3. Filter by gender, level, or hostel

#### Add Student
1. Click **Add Student**
2. Link to Django user account
3. Enter matric number and details
4. Save

### Reports & Statistics

1. Go to **Allocation Overview**
2. View:
   - Total occupancy rate
   - Per-hostel statistics
   - Available rooms
   - Allocation status breakdown

---

## Troubleshooting

### Issue: Virtual Environment Not Activating

**Windows PowerShell Error**: `cannot be loaded because running scripts is disabled`

**Solution**:
```powershell
# Run as Administrator, then execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
.\venv\Scripts\Activate.ps1
```

### Issue: "Port 8000 already in use"

**Solution**:
```bash
# Use a different port
python manage.py runserver 8001

# Or find and kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Issue: Database Migration Errors

**Solution**:
```bash
# Reset database (WARNING: This deletes all data)
python manage.py migrate hostels zero
python manage.py migrate

# Or create fresh database
rm db.sqlite3
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
```

### Issue: Matric Number Login Not Working

**Ensure**:
1. StudentProfile is created for the user
2. Matric number is entered correctly (case-sensitive)
3. Password is correct
4. Custom authentication backend is enabled in settings

### Issue: "ModuleNotFoundError" When Running Server

**Solution**:
```bash
# Ensure virtual environment is activated
# Windows: .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Static Files Not Loading (CSS/Icons)

**Solution**:
```bash
# Collect static files
python manage.py collectstatic --noinput
```

---

## FAQ

### Q: How do I reset a student's password?

**A**: 
```bash
python manage.py changepassword <username>
```

### Q: Can I change a student's matric number after creation?

**A**: Yes, through the admin panel:
1. Go to Admin → Students
2. Click the student's name
3. Edit matric number
4. Save

### Q: How do I backup the database?

**A**: 
```bash
# For SQLite
cp db.sqlite3 db.sqlite3.backup

# For PostgreSQL
pg_dump -U postgres hostel_management > backup.sql
```

### Q: Can multiple students be allocated to the same room?

**A**: Yes, up to the room's capacity. The system ensures:
- Maximum occupancy is respected
- Gender consistency is maintained
- Room preferences are honored

### Q: How do I export hostel request data?

**A**: 
```bash
# Export to CSV
python manage.py dumpdata hostels.HostelRequest --format=json > requests.json

# Or use admin export feature (if available)
```

### Q: What happens if a student's request is rejected?

**A**: 
- Student receives notification
- Can submit a new request after rejection
- Can request a different hostel

### Q: Is there a limit on hostel requests per student?

**A**: Currently, students can have one active request (Pending or Approved). They must complete or reject this before submitting another.

### Q: How do I add test data?

**A**:
```bash
python manage.py loaddata fixtures/initial_data.json
```

### Q: Can I change the color scheme?

**A**: Yes! The colors are defined in templates. Main colors are in `templates/base.html` and `templates/home.html`. Look for color codes like `#0f766e` (teal).

### Q: How do I enable production mode?

**A**:
1. Update `.env`: `DEBUG=False`
2. Set appropriate `ALLOWED_HOSTS`
3. Use production database (PostgreSQL recommended)
4. Set `SECURE_SSL_REDIRECT=True`
5. Use production WSGI server (Gunicorn)

### Q: How do I update the application?

**A**:
```bash
# Pull latest changes
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Restart server
python manage.py runserver
```

---

## Support & Contact

For issues or questions:
1. Check the Troubleshooting section
2. Review error messages in server console
3. Check Django documentation: https://docs.djangoproject.com/
4. Contact system administrator

---

## Version Information

- **Application Version**: 1.0.0
- **Django Version**: 5.2.1
- **Python Version**: 3.8+
- **Last Updated**: January 9, 2026

---

## License

This project is proprietary to Trinity University. Unauthorized reproduction or distribution is prohibited.

---

**Happy Using! 🎓**
