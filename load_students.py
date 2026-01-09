#!/usr/bin/env python
"""
Auto-load students, hostels and rooms during deployment.
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
from hostels.models import StudentProfile, Hostel, Floor, Room

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

def create_hostels_and_rooms():
    """Create hostels and rooms matching fixture format"""
    print("\n🏠 Creating Hostels and Rooms...")
    
    hostels_data = [
        {'name': 'Mary', 'gender': 'F'},
        {'name': 'Esther', 'gender': 'F'},
        {'name': 'Deborah', 'gender': 'F'},
        {'name': 'Dorcas', 'gender': 'F'},
        {'name': 'Daniel', 'gender': 'M'},
        {'name': 'Joseph', 'gender': 'M'},
    ]
    
    floor_types = ['GF', 'FF', 'SF']  # Ground Floor, First Floor, Second Floor
    room_capacities = [2, 2, 4, 6]  # 4 rooms per floor
    
    created_hostels = 0
    created_floors = 0
    created_rooms = 0
    
    for hostel_data in hostels_data:
        try:
            # Create hostel if it doesn't exist
            hostel, created = Hostel.objects.get_or_create(
                name=hostel_data['name'],
                defaults={
                    'gender': hostel_data['gender'],
                    'description': f"{hostel_data['gender']} hostel - {hostel_data['name']}"
                }
            )
            
            if created:
                print(f"✅ Hostel: {hostel_data['name']} ({hostel_data['gender']})")
                created_hostels += 1
            else:
                print(f"⚠️  Hostel {hostel_data['name']} already exists")
            
            # Create floors and rooms
            for floor_type in floor_types:
                try:
                    floor, floor_created = Floor.objects.get_or_create(
                        hostel=hostel,
                        floor_type=floor_type,
                        defaults={}
                    )
                    
                    if floor_created:
                        created_floors += 1
                    
                    # Create 4 rooms per floor with different capacities
                    for idx, capacity in enumerate(room_capacities, 1):
                        try:
                            room_number = f"{floor_type}-{idx:02d}"
                            room, room_created = Room.objects.get_or_create(
                                floor=floor,
                                room_number=room_number,
                                defaults={'capacity': capacity}
                            )
                            
                            if room_created:
                                created_rooms += 1
                        
                        except Exception as e:
                            print(f"  ❌ Error creating room {room_number}: {str(e)}")
                
                except Exception as e:
                    print(f"  ❌ Error creating floor {floor_type}: {str(e)}")
        
        except Exception as e:
            print(f"❌ Error creating hostel {hostel_data['name']}: {str(e)}")
    
    print(f"\n📊 Hostels/Rooms Summary:")
    print(f"   Hostels: {created_hostels}")
    print(f"   Floors: {created_floors}")
    print(f"   Rooms: {created_rooms}")
    
    return True

def load_students_from_csv(csv_file='students.csv'):
    """Load students from CSV file"""
    
    csv_path = Path(csv_file)
    
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_file}")
        return False
    
    print(f"\n📂 Loading students from: {csv_file}")
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
                    
                    # Extract first name for password
                    name_parts = full_name.strip().split()
                    first_name_part = name_parts[0] if name_parts else 'Password123'
                    password = first_name_part.capitalize()  # First name as password
                    
                    # Split full name properly
                    first_name = ' '.join(name_parts[:-1]) if len(name_parts) > 1 else name_parts[0] if name_parts else ''
                    last_name = name_parts[-1] if name_parts else ''
                    
                    # Create user
                    user = User.objects.create_user(
                        username=matric_no,
                        email=f'{matric_no}@trinity.edu',
                        password=password,
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
                    
                    print(f"✅ {matric_no}: {full_name} - Password: {password}")
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
    print("Trinity Hostel Management - Auto Setup")
    print("=" * 70)
    print()
    
    # Create superuser first
    print("📌 Creating superuser...")
    create_superuser()
    
    # Create hostels and rooms
    create_hostels_and_rooms()
    
    # Load students
    success = load_students_from_csv('students.csv')
    exit(0 if success else 1)
