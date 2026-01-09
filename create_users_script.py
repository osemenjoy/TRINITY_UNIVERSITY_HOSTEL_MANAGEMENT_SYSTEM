#!/usr/bin/env python
"""
Script to create test students and superuser on Render.
Run this in Render Shell or locally in Django shell.

Usage in Render Shell:
    python manage.py shell < create_users_script.py

Or interactively:
    python manage.py shell
    >>> exec(open('create_users_script.py').read())
"""

from django.contrib.auth.models import User
from hostels.models import StudentProfile

def create_superuser():
    """Create admin superuser"""
    if User.objects.filter(username='admin').exists():
        print("❌ Admin already exists")
        return False
    
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@trinity.edu',
        password='admin123456'  # Change this!
    )
    print(f"✅ Superuser created!")
    print(f"   Username: admin")
    print(f"   Password: admin123456")
    return True

def create_students(count=10, password='studentpass123'):
    """Create multiple test students"""
    genders = ['M', 'F']
    levels = ['100', '200', '300', '400']
    
    created = []
    
    for i in range(1, count + 1):
        username = f'stu{i:03d}'
        matric_no = f'STU{i:03d}'
        
        # Skip if user exists
        if User.objects.filter(username=username).exists():
            print(f"⚠️  {username} already exists, skipping...")
            continue
        
        try:
            user = User.objects.create_user(
                username=username,
                email=f'{username}@trinity.edu',
                password=password
            )
            
            student = StudentProfile.objects.create(
                user=user,
                matric_no=matric_no,
                gender=genders[i % 2],
                level=levels[i % 4]
            )
            
            created.append({
                'username': username,
                'matric_no': matric_no,
                'email': f'{username}@trinity.edu',
                'password': password
            })
            
            print(f"✅ Created: {username} ({matric_no}) - Level {student.level}")
            
        except Exception as e:
            print(f"❌ Error creating {username}: {str(e)}")
    
    return created

def create_single_student(username, matric_no, gender='M', level='100', password='studentpass123'):
    """Create a single student"""
    if User.objects.filter(username=username).exists():
        print(f"❌ User {username} already exists")
        return None
    
    try:
        user = User.objects.create_user(
            username=username,
            email=f'{username}@trinity.edu',
            password=password
        )
        
        student = StudentProfile.objects.create(
            user=user,
            matric_no=matric_no,
            gender=gender,
            level=level
        )
        
        print(f"✅ Student created!")
        print(f"   Username: {username}")
        print(f"   Matric No: {matric_no}")
        print(f"   Gender: {gender}")
        print(f"   Level: {level}")
        print(f"   Password: {password}")
        
        return student
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def list_all_users():
    """List all users and students"""
    print("\n=== ALL USERS ===")
    users = User.objects.all()
    if not users.exists():
        print("No users found")
        return
    
    for user in users:
        print(f"- {user.username} ({user.email}) - Admin: {user.is_staff}")
    
    print("\n=== ALL STUDENTS ===")
    students = StudentProfile.objects.all()
    if not students.exists():
        print("No students found")
        return
    
    for student in students:
        print(f"- {student.matric_no} ({student.user.username}) - Level: {student.level}")

def delete_user(username):
    """Delete a user"""
    try:
        user = User.objects.get(username=username)
        user.delete()
        print(f"✅ User {username} deleted")
        return True
    except User.DoesNotExist:
        print(f"❌ User {username} not found")
        return False

# ===== RUN SCRIPT =====
if __name__ == '__main__':
    print("=" * 50)
    print("Trinity Hostel Management - User Creation Script")
    print("=" * 50)
    print()
    
    # Create superuser
    print("1️⃣  Creating superuser...")
    create_superuser()
    print()
    
    # Create students
    print("2️⃣  Creating 10 test students...")
    students = create_students(count=10, password='studentpass123')
    print()
    
    # List all users
    print("3️⃣  Listing all users...")
    list_all_users()
    
    print()
    print("=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print()
    print("Login Credentials:")
    print("- Admin: admin / admin123456")
    print("- Students: stu001-stu010 / studentpass123")
    print()
