# QUICK START GUIDE

## Trinity Hostel Management System - 5 Minute Setup

### Prerequisites
- Python 3.8+ installed
- Django already installed in the project

### Quick Setup

1. **Open PowerShell/Terminal in the project folder**
   ```powershell
   cd c:\Users\Osemen\Documents\hostelredo
   ```

2. **Run migrations** (if not done)
   ```powershell
   python manage.py migrate
   ```

3. **Load test data** (hostels, floors, rooms)
   ```powershell
   python manage.py loaddata hostels/fixtures/hostels_and_floors.json hostels/fixtures/rooms.json
   ```

4. **Create admin user**
   ```powershell
   python manage.py createsuperuser
   ```
   When prompted, enter:
   - Username: `admin`
   - Email: `admin@trinity.edu`
   - Password: (choose your password)

5. **Start the server**
   ```powershell
   python manage.py runserver
   ```

6. **Access the application**
   - Go to: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

### Test Accounts (Already Created)

**Student 1 (Male)**
- Username: `jdoe`
- Password: `password123`
- Hostel Access: Male hostels only (Daniel, Joseph)

**Student 2 (Female)**
- Username: `ajones`
- Password: `password123`
- Hostel Access: Female hostels only (Mary, Esther, Deborah, Dorcas)

### Testing Workflow

1. **Login as Student (jdoe)**
   - http://127.0.0.1:8000/student/dashboard/
   - Click "Request Hostel"
   - Select "Daniel" hostel
   - Choose room capacity "4 persons"
   - Submit request

2. **Login as Admin (admin)**
   - http://127.0.0.1:8000/admin/requests/
   - See the pending request from John Doe
   - Click "Approve" button
   - System automatically allocates a room

3. **View as Student Again**
   - Go back to dashboard
   - See the allocated room details

4. **Check Allocations**
   - Admin: http://127.0.0.1:8000/admin/allocations/
   - See occupancy statistics and all allocations

### Project Structure

```
hostelredo/
├── hostels/                        # Main app
│   ├── models.py                   # Database models
│   ├── views.py                    # View logic
│   ├── forms.py                    # Form handling
│   ├── urls.py                     # URL routing
│   ├── admin.py                    # Admin interface
│   ├── fixtures/                   # Preloaded data
│   │   ├── hostels_and_floors.json
│   │   └── rooms.json
│   └── migrations/                 # Database migrations
├── hostel_management/              # Project settings
│   ├── settings.py                 # Configuration
│   ├── urls.py                     # Main URL routing
│   └── wsgi.py                     # WSGI for deployment
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   └── hostels/
│       ├── student_dashboard.html
│       ├── request_hostel.html
│       ├── admin_requests.html
│       └── allocation_overview.html
├── static/                         # CSS, JS, images
├── manage.py                       # Django CLI
├── db.sqlite3                      # SQLite database
├── README.md                       # Full documentation
├── DEPLOYMENT.md                   # Production deployment
└── requirements.txt                # Python dependencies
```

### Key Features

✅ **Student Dashboard** - View request status and current allocation
✅ **Request Hostel** - Submit hostel request filtered by gender
✅ **Admin Management** - View and approve/reject requests
✅ **Automatic Allocation** - System finds available rooms automatically
✅ **Occupancy Tracking** - Real-time bed availability
✅ **Data Validation** - Gender matching, capacity limits, one request per student
✅ **Bootstrap 5 UI** - Modern, responsive design
✅ **Admin Interface** - Full Django admin for data management

### Stopping the Server

Press `Ctrl + C` in the terminal

### Common Commands

```powershell
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Load fixtures
python manage.py loaddata hostels/fixtures/hostels_and_floors.json

# Check for issues
python manage.py check

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Export data
python manage.py dumpdata > backup.json

# Import data
python manage.py loaddata backup.json
```

### Deployment

See `DEPLOYMENT.md` for detailed production deployment steps on Render.

### Need Help?

Refer to:
- `README.md` - Complete documentation
- `DEPLOYMENT.md` - Production deployment
- `hostels/models.py` - Database model definitions
- Django Docs: https://docs.djangoproject.com/en/5.2/

---

**Created**: January 9, 2026
**Version**: 1.0
**Status**: Production Ready
