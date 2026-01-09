# Trinity University Hostel Management System

A comprehensive Django 5 web application for managing student hostel requests and admin approval workflows. This system streamlines the hostel allocation process for Trinity University with features for students to request hostels and admins to manage and approve allocations.

## Features

### Student Features
- **User Authentication**: Secure login system linked to Django User model
- **Student Profile**: Matric number, gender, and level information
- **Hostel Request**: Students can submit requests for preferred hostels filtered by gender
- **Dashboard**: View current request status and room allocation
- **Available Beds Display**: See remaining available beds per hostel before requesting

### Admin Features
- **Request Management**: View, filter, and manage all student requests
- **Request Actions**: Approve/reject requests with automatic room allocation
- **Allocation Overview**: Dashboard showing hostel occupancy statistics and all allocations
- **Admin Panel**: Full Django admin interface for data management

### System Features
- **Gender-based Hostel Filtering**: Only show hostels matching student's gender
- **Automatic Room Assignment**: Find available rooms matching student preferences
- **Occupancy Tracking**: Real-time tracking of room capacity and availability
- **Data Validation**: Prevent double requests, gender mismatches, and over-capacity allocations
- **Bootstrap 5 UI**: Responsive and modern user interface

## Hostels

The system comes preloaded with:

**Female Hostels**: Mary, Esther, Deborah, Dorcas  
**Male Hostels**: Daniel, Joseph

Each hostel has:
- 3 Floors: Ground Floor (GF), First Floor (FF), Second Floor (SF)
- 4 Rooms per floor: 2 with 2-person capacity, 1 with 4-person capacity, 1 with 6-person capacity
- **Total: 72 rooms across all hostels**

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Setup Steps

1. **Clone/Extract the project**
   ```bash
   cd hostelredo
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install Django**
   ```bash
   pip install django
   ```

4. **Run migrations** (already done)
   ```bash
   python manage.py migrate
   ```

5. **Load initial data** (hostels, floors, rooms)
   ```bash
   python manage.py loaddata hostels/fixtures/hostels_and_floors.json hostels/fixtures/rooms.json
   ```

6. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

7. **Create test student users** (optional)
   ```bash
   python manage.py shell
   ```
   Then in the shell:
   ```python
   from django.contrib.auth.models import User
   from hostels.models import StudentProfile

   # Create a male student
   user1 = User.objects.create_user(
       username='jdoe',
       password='password123',
       first_name='John',
       last_name='Doe',
       email='jdoe@trinity.edu'
   )
   StudentProfile.objects.create(
       user=user1,
       matric_no='TRN2024001',
       gender='M',
       level='100'
   )

   # Create a female student
   user2 = User.objects.create_user(
       username='ajones',
       password='password123',
       first_name='Amy',
       last_name='Jones',
       email='ajones@trinity.edu'
   )
   StudentProfile.objects.create(
       user=user2,
       matric_no='TRN2024002',
       gender='F',
       level='100'
   )
   
   exit()
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   - **Main Site**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/ (login with superuser)

## URLs

### Student URLs
- `/student/dashboard/` - View request status and allocation
- `/student/request-hostel/` - Submit a new hostel request

### Admin URLs
- `/admin/requests/` - Manage all hostel requests
- `/admin/allocations/` - View allocation overview and statistics
- `/admin/` - Django admin interface

## Project Structure

```
hostelredo/
├── hostel_management/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── hostels/                    # Main application
│   ├── migrations/             # Database migrations
│   ├── fixtures/               # Preloaded data
│   │   ├── hostels_and_floors.json
│   │   └── rooms.json
│   ├── models.py              # Database models
│   ├── views.py               # View logic
│   ├── forms.py               # Form definitions
│   ├── urls.py                # URL routing
│   ├── admin.py               # Admin interface
│   └── apps.py
├── templates/                 # HTML templates
│   ├── base.html              # Base template
│   └── hostels/               # App-specific templates
│       ├── student_dashboard.html
│       ├── request_hostel.html
│       ├── admin_requests.html
│       └── allocation_overview.html
├── static/                    # Static files (CSS, JS, images)
├── manage.py                  # Django CLI
└── db.sqlite3                # SQLite database
```

## Database Models

### StudentProfile
- `user` (OneToOne with User)
- `matric_no` (unique identifier)
- `gender` (M/F)
- `level` (100/200/300/400)

### Hostel
- `name` (unique)
- `gender` (M/F)
- `description`
- `get_available_beds()` method

### Floor
- `hostel` (ForeignKey)
- `floor_type` (GF/FF/SF)

### Room
- `floor` (ForeignKey)
- `room_number`
- `capacity` (2/4/6)
- `current_occupancy`
- `is_full()` method
- `available_beds()` method

### HostelRequest
- `student` (ForeignKey to StudentProfile)
- `hostel` (ForeignKey)
- `preferred_capacity` (2/4/6)
- `status` (PENDING/APPROVED/REJECTED)
- `note` (optional)
- Validation: gender match, one active request per student

### Allocation
- `student` (OneToOne with StudentProfile)
- `room` (ForeignKey)
- `date_allocated`
- `notes`
- Validation: room capacity, gender match

## API/Request Flow

### Student Request Flow
1. Student logs in
2. Visits `/student/dashboard/` to see current status
3. Clicks "Request Hostel" link
4. Selects hostel (filtered by gender), room capacity, and optional notes
5. System validates:
   - Gender matches
   - No active requests exist
   - All required fields filled
6. Request saved as PENDING
7. Student sees "Your request is pending admin approval"

### Admin Approval Flow
1. Admin logs in and visits `/admin/requests/`
2. Sees list of PENDING, APPROVED, and REJECTED requests
3. Clicks "Approve" button for a pending request
4. System automatically:
   - Finds available room matching capacity
   - Creates Allocation record
   - Updates room occupancy
   - Changes request status to APPROVED
5. Admin sees success message
6. Student sees "You are allocated to [Hostel], [Floor], Room [Number]"

## Validation Rules

- ✅ Student gender must match hostel gender
- ✅ Student can only have one active (PENDING or APPROVED) request
- ✅ Room cannot exceed its capacity
- ✅ Students cannot be allocated to wrong gender hostels
- ✅ Each student gets only one allocation

## Deployment (Render Free Tier)

### Prerequisites
- PostgreSQL database (Render provides free tier)
- GitHub account (for code repository)

### Steps

1. **Update settings.py for production**
   ```python
   # settings.py
   import dj_database_url
   
   DEBUG = False
   ALLOWED_HOSTS = ['your-app-name.onrender.com']
   
   DATABASES = {
       'default': dj_database_url.config(
           default='postgresql://...',
           conn_max_age=600
       )
   }
   
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

2. **Create requirements.txt**
   ```bash
   pip freeze > requirements.txt
   ```
   Add these lines:
   ```
   gunicorn==21.2.0
   dj-database-url==2.1.0
   whitenoise==6.6.0
   psycopg2-binary==2.9.9
   ```

3. **Create Render Web Service**
   - Go to https://render.com
   - Connect GitHub repository
   - Select Python as environment
   - Set build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata hostels/fixtures/hostels_and_floors.json hostels/fixtures/rooms.json`
   - Set start command: `gunicorn hostel_management.wsgi:application`

4. **Set environment variables in Render**
   ```
   DJANGO_SUPERUSER_USERNAME = admin
   DJANGO_SUPERUSER_PASSWORD = your_secure_password
   DJANGO_SUPERUSER_EMAIL = admin@trinity.edu
   SECRET_KEY = your_django_secret_key
   DEBUG = False
   ```

5. **Create superuser on deployed instance**
   ```bash
   python manage.py createsuperuser
   ```

## Testing

### Create test data
```python
python manage.py shell
from django.contrib.auth.models import User
from hostels.models import *

# Create students (see Setup section above)

# Then via admin panel:
# 1. Approve a request
# 2. Check if allocation was created
# 3. View allocation overview
```

### Manual testing checklist
- [ ] Login as student
- [ ] View dashboard
- [ ] Submit hostel request (select hostel, capacity, optional note)
- [ ] Verify request is PENDING
- [ ] Login as admin
- [ ] View all requests
- [ ] Filter by hostel
- [ ] Filter by status
- [ ] Approve a request
- [ ] Verify room occupancy increased
- [ ] Verify student can see allocation
- [ ] Check allocation overview statistics
- [ ] Reject a request
- [ ] Verify student can submit new request

## Troubleshooting

**Issue**: Database migration errors
**Solution**: 
```bash
python manage.py makemigrations
python manage.py migrate
```

**Issue**: Fixtures not loading
**Solution**:
```bash
python manage.py loaddata hostels/fixtures/hostels_and_floors.json
python manage.py loaddata hostels/fixtures/rooms.json
```

**Issue**: Students can't see hostels on request form
**Solution**: Check if StudentProfile exists for the user and gender is set correctly

**Issue**: Room not allocated on approval
**Solution**: Check if rooms exist and have capacity available

## License

This project is proprietary to Trinity University.

## Support

For issues or questions, contact the IT department.
#   T R I N I T Y _ U N I V E R S I T Y _ H O S T E L _ M A N A G E M E N T _ S Y S T E M  
 