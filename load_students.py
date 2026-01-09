#!/usr/bin/env python
"""
Auto-load students from CSV during deployment.
This script runs during the build/release phase on Render.

Usage:
    python load_students.py
"""

import os
import django
import csv
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_management.settings')
django.setup()

from django.contrib.auth.models import User
from hostels.models import StudentProfile

def create_superuser():
    """Create admin superuser if it doesn't exist"""
    if User.objects.filter(username='admin').exists():
        print("⚠️  Admin already exists, skipping")
        return False
    
    try:
        User.objects.create_superuser(
            username='admin',
            email='admin@trinity.edu',
            password='admin123456'
        )
        print("✅ Admin created: admin / admin123456")
        return True
    except Exception as e:
        print(f"❌ Error creating admin: {str(e)}")
        return False

def load_students_from_csv(csv_file='students.csv'):
    """Load students from CSV file"""
    
    csv_path = Path(csv_file)
    
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_file}")
        return False
    
    print(f"📂 Loading students from: {csv_file}")
    created_count = 0
    skipped_count = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    full_name = row.get('full_name', '').strip()
                    matric_no = row.get('matric_no', '').strip()
                    gender = row.get('gender', 'M').strip().upper()
                    level = row.get('level', '100').strip()
                    
                    if not full_name or not matric_no:
                        print(f"⚠️  Skipping row with missing data: {row}")
                        continue
                    
                    # Check if user already exists
                    if User.objects.filter(username=matric_no).exists():
                        print(f"⚠️  {matric_no} already exists, skipping")
                        skipped_count += 1
                        continue
                    
                    # Extract surname for password
                    name_parts = full_name.strip().split()
                    surname = name_parts[-1].capitalize() if name_parts else 'Password123'
                    
                    # Split full name
                    first_name = ' '.join(name_parts[:-1]) if len(name_parts) > 1 else name_parts[0] if name_parts else ''
                    last_name = name_parts[-1] if name_parts else ''
                    
                    # Create user
                    user = User.objects.create_user(
                        username=matric_no,
                        email=f'{matric_no}@trinity.edu',
                        password=surname,
                        first_name=first_name,
                        last_name=last_name
                    )
                    
                    # Create student profile
                    StudentProfile.objects.create(
                        user=user,
                        matric_no=matric_no,
                        gender=gender,
                        level=level
                    )
                    
                    print(f"✅ {matric_no}: {full_name} - Password: {surname}")
                    created_count += 1
                
                except Exception as e:
                    print(f"❌ Error creating {matric_no}: {str(e)}")
                    continue
        
        print()
        print("=" * 70)
        print(f"✅ Student Loading Complete!")
        print(f"   Created: {created_count}")
        print(f"   Skipped: {skipped_count}")
        print("=" * 70)
        
        return True
    
    except Exception as e:
        print(f"❌ Error reading CSV: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 70)
    print("Trinity Hostel Management - Auto Student Loader")
    print("=" * 70)
    print()
    
    # Create superuser first
    print("📌 Creating superuser...")
    create_superuser()
    print()
    
    # Load students
    success = load_students_from_csv('students.csv')
    exit(0 if success else 1)
