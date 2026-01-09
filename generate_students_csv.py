#!/usr/bin/env python
"""
Generate student CSV file with custom data.
Run this to create students.csv with your student data.

Usage:
    python generate_students_csv.py
"""

import csv
import os

def generate_csv(filename='students.csv'):
    """Generate a sample students.csv file"""
    
    students = [
        {
            'full_name': 'John Oladele Doe',
            'matric_no': 'STU001',
            'gender': 'M',
            'level': '100'
        },
        {
            'full_name': 'Alice Oluwatoyin Johnson',
            'matric_no': 'STU002',
            'gender': 'F',
            'level': '100'
        },
        {
            'full_name': 'Michael Chukwuma Smith',
            'matric_no': 'STU003',
            'gender': 'M',
            'level': '200'
        },
        {
            'full_name': 'Sarah Akinyi Williams',
            'matric_no': 'STU004',
            'gender': 'F',
            'level': '200'
        },
        {
            'full_name': 'David Tunde Brown',
            'matric_no': 'STU005',
            'gender': 'M',
            'level': '300'
        },
        {
            'full_name': 'Emily Chioma Davis',
            'matric_no': 'STU006',
            'gender': 'F',
            'level': '300'
        },
        {
            'full_name': 'James Oluwaseun Wilson',
            'matric_no': 'STU007',
            'gender': 'M',
            'level': '400'
        },
        {
            'full_name': 'Jessica Amara Martinez',
            'matric_no': 'STU008',
            'gender': 'F',
            'level': '400'
        },
    ]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['full_name', 'matric_no', 'gender', 'level']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(students)
        
        print(f"✅ Generated: {filename}")
        print(f"   Total students: {len(students)}")
        print(f"\n📝 Students created:")
        for s in students:
            password = s['full_name'].split()[-1].capitalize()
            print(f"   - {s['full_name']} ({s['matric_no']}) → Password: {password}")
        
        print(f"\n🚀 Next step: Upload {filename} to Render or use:")
        print(f"   python manage.py create_students_custom --csv {filename}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def custom_csv(filename='custom_students.csv'):
    """Create empty template for user to fill in"""
    
    template = [
        {
            'full_name': 'First Last Name',
            'matric_no': 'STU001',
            'gender': 'M',
            'level': '100'
        },
        {
            'full_name': 'Another Student',
            'matric_no': 'STU002',
            'gender': 'F',
            'level': '100'
        },
    ]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['full_name', 'matric_no', 'gender', 'level']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(template)
        
        print(f"✅ Template created: {filename}")
        print(f"\n📝 Edit this file and fill in your student data:")
        print(f"   - full_name: Student's full name")
        print(f"   - matric_no: Matric number (e.g., STU001)")
        print(f"   - gender: M or F")
        print(f"   - level: 100, 200, 300, or 400")
        print(f"\n🚀 Then run:")
        print(f"   python manage.py create_students_custom --csv {filename}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("Student CSV Generator")
    print("=" * 60)
    print()
    
    choice = input("1. Generate sample students (8 default)\n2. Create empty template\n\nChoice (1 or 2): ").strip()
    
    if choice == '2':
        custom_csv()
    else:
        generate_csv()
    
    print()
