# Creating Superuser & Students on Render Cloud

## ⚠️ Problem: "Invalid Credentials"

You're seeing "Invalid Credentials" because:
- No superuser exists yet on Render
- No student accounts exist yet
- Registration is disabled (students only login)

---

## Method 1: Using Render Shell (Easiest) ✅

### Step 1: Open Render Shell
1. Go to your Render dashboard
2. Click on your Web Service (trinity-hostel-management)
3. Go to **Shell** tab
4. You'll see a terminal in your browser

### Step 2: Create Superuser
```bash
python manage.py createsuperuser
```

When prompted, enter:
```
Username: admin
Email: admin@trinity.edu
Password: (your-strong-password)
Password (again): (repeat-password)
```

**✅ Superuser created!** You can now login to `/admin` with these credentials.

### Step 3: Create Student Accounts

#### Option A: Create One Student Manually
```bash
python manage.py shell
```

Then type these commands in the Python shell:
```python
from django.contrib.auth.models import User
from hostels.models import StudentProfile

# Create user
user = User.objects.create_user(
    username='stu001',
    email='stu001@trinity.edu',
    password='studentpass123'
)

# Create student profile with matric number
student = StudentProfile.objects.create(
    user=user,
    matric_no='STU001',
    gender='M',
    level='100'
)

print("Student created successfully!")
print(f"Login with: {user.username} / studentpass123")
print(f"Or: {student.matric_no} / studentpass123")
exit()
```

#### Option B: Create Multiple Students (Bulk)
```bash
python manage.py shell
```

Then paste this code:
```python
from django.contrib.auth.models import User
from hostels.models import StudentProfile

# Create 5 test students
students_data = [
    {'username': 'stu001', 'email': 'stu001@trinity.edu', 'matric_no': 'STU001', 'gender': 'M', 'level': '100'},
    {'username': 'stu002', 'email': 'stu002@trinity.edu', 'matric_no': 'STU002', 'gender': 'F', 'level': '100'},
    {'username': 'stu003', 'email': 'stu003@trinity.edu', 'matric_no': 'STU003', 'gender': 'M', 'level': '200'},
    {'username': 'stu004', 'email': 'stu004@trinity.edu', 'matric_no': 'STU004', 'gender': 'F', 'level': '200'},
    {'username': 'stu005', 'email': 'stu005@trinity.edu', 'matric_no': 'STU005', 'gender': 'M', 'level': '300'},
]

password = 'studentpass123'

for data in students_data:
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=password
    )
    
    StudentProfile.objects.create(
        user=user,
        matric_no=data['matric_no'],
        gender=data['gender'],
        level=data['level']
    )
    
    print(f"✅ Created: {data['username']} ({data['matric_no']})")

print("\n✅ All students created!")
print(f"Login password for all: {password}")
exit()
```

---

## Method 2: Using Django Fixture (Best for Future Deployments)

### Step 1: Create Fixture File Locally
Create `hostels/fixtures/students.json`:

```json
[
  {
    "model": "auth.user",
    "pk": 1,
    "fields": {
      "username": "stu001",
      "email": "stu001@trinity.edu",
      "password": "pbkdf2_sha256$260000$abcdefghijk$hash_value_here",
      "first_name": "John",
      "last_name": "Doe",
      "is_staff": false,
      "is_active": true
    }
  },
  {
    "model": "hostels.studentprofile",
    "pk": 1,
    "fields": {
      "user": 1,
      "matric_no": "STU001",
      "gender": "M",
      "level": "100"
    }
  }
]
```

### Step 2: Load on Render
In Render Shell:
```bash
python manage.py loaddata hostels/fixtures/students.json
```

---

## Test Credentials After Creating

### Login as Admin
- **URL**: https://your-app-name.onrender.com/admin
- **Username**: admin
- **Password**: (the one you set)

### Login as Student
- **URL**: https://your-app-name.onrender.com/accounts/login/
- **Matric Number**: STU001 (or STU002, etc.)
- **Password**: studentpass123

---

## Render Shell Steps (Visual Guide)

1. Dashboard → Select your Web Service
2. Click **Shell** tab
3. You'll see: `$`
4. Type commands there

**Example:**
```
$ python manage.py createsuperuser
Username: admin
Email: admin@trinity.edu
Password: 
Password (again):
Superuser created successfully.
$ 
```

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Create superuser | `python manage.py createsuperuser` |
| Create student | `python manage.py shell` + Python code above |
| List all users | `python manage.py shell` → `from django.contrib.auth.models import User; User.objects.all()` |
| List students | `python manage.py shell` → `from hostels.models import StudentProfile; StudentProfile.objects.all()` |
| Delete user | `python manage.py shell` → `User.objects.get(username='stu001').delete()` |
| Exit shell | `exit()` or `Ctrl+D` |

---

## Why "Invalid Credentials"?

✅ **Fixed by:**
- Creating superuser in Render Shell
- Creating student accounts before they try to login
- Using correct matric_no or username

---

## Next Steps

1. **Create Superuser** (Render Shell)
2. **Create 5-10 Test Students** (Render Shell)
3. **Test Login** with student credentials
4. **Add Hostels/Rooms** in admin panel if needed
5. **Approve Requests** as admin

---

## Pro Tip: Automate with Management Command

Create `hostels/management/commands/create_test_students.py`:

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hostels.models import StudentProfile

class Command(BaseCommand):
    help = 'Create test student accounts'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of students to create')

    def handle(self, *args, **options):
        count = options['count']
        for i in range(1, count + 1):
            username = f'stu{i:03d}'
            user = User.objects.create_user(
                username=username,
                email=f'{username}@trinity.edu',
                password='studentpass123'
            )
            StudentProfile.objects.create(
                user=user,
                matric_no=f'STU{i:03d}',
                gender='M' if i % 2 == 0 else 'F',
                level=str((i % 4) * 100 + 100)
            )
            self.stdout.write(f'✅ Created {username}')
```

Then run on Render:
```bash
python manage.py create_test_students 10
```

---

## Support

- **Render Docs**: https://render.com/docs/shell
- **Django Docs**: https://docs.djangoproject.com/en/5.2/ref/django-admin/
- **Still stuck?** Check Render logs: Web Service → **Logs** tab
