from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hostels.models import StudentProfile
import csv
import os


class Command(BaseCommand):
    help = 'Create students with custom names and matric numbers. Password = surname with capital first letter'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            help='Path to CSV file with student data (name, matric_no, gender, level)'
        )
        parser.add_argument(
            '--name',
            type=str,
            help='Full name of single student (e.g., "John Doe")'
        )
        parser.add_argument(
            '--matric',
            type=str,
            help='Matric number (e.g., "STU001")'
        )
        parser.add_argument(
            '--gender',
            type=str,
            default='M',
            choices=['M', 'F'],
            help='Gender (M or F, default: M)'
        )
        parser.add_argument(
            '--level',
            type=str,
            default='100',
            choices=['100', '200', '300', '400'],
            help='Level (100, 200, 300, 400, default: 100)'
        )
        parser.add_argument(
            '--admin',
            action='store_true',
            help='Create admin/superuser'
        )

    def extract_surname(self, full_name):
        """Extract surname and capitalize it for password"""
        parts = full_name.strip().split()
        if len(parts) > 0:
            surname = parts[-1]  # Last name is surname
            return surname.capitalize()
        return 'Password123'

    def create_student_from_data(self, full_name, matric_no, gender, level):
        """Create a student with given data"""
        # Extract username from matric number (lowercase)
        username = matric_no.lower()
        
        # Extract surname for password
        password = self.extract_surname(full_name)
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'⚠️  {username} already exists, skipping'))
            return None
        
        try:
            # Split full name
            name_parts = full_name.strip().split()
            first_name = ' '.join(name_parts[:-1]) if len(name_parts) > 1 else name_parts[0]
            last_name = name_parts[-1] if len(name_parts) > 0 else ''
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=f'{username}@trinity.edu',
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create student profile
            student = StudentProfile.objects.create(
                user=user,
                matric_no=matric_no,
                gender=gender,
                level=level
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ {full_name} ({matric_no}) - Username: {username}, Password: {password}'
                )
            )
            return student
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating {full_name}: {str(e)}')
            )
            return None

    def handle_csv(self, csv_path):
        """Handle CSV file with student data"""
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'❌ File not found: {csv_path}'))
            return
        
        self.stdout.write(f'\n📂 Reading students from: {csv_path}')
        created_count = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Expected columns: full_name, matric_no, gender, level
                for row in reader:
                    try:
                        full_name = row.get('full_name', '').strip()
                        matric_no = row.get('matric_no', '').strip()
                        gender = row.get('gender', 'M').strip().upper()
                        level = row.get('level', '100').strip()
                        
                        if not full_name or not matric_no:
                            self.stdout.write(self.style.WARNING(
                                f'⚠️  Skipping row with missing name or matric: {row}'
                            ))
                            continue
                        
                        student = self.create_student_from_data(full_name, matric_no, gender, level)
                        if student:
                            created_count += 1
                    
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'❌ Error processing row: {str(e)}'))
                        continue
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error reading CSV: {str(e)}'))
            return
        
        return created_count

    def handle_single_student(self, full_name, matric_no, gender, level):
        """Handle creating a single student"""
        self.stdout.write(f'\n👤 Creating single student...')
        student = self.create_student_from_data(full_name, matric_no, gender, level)
        return 1 if student else 0

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Trinity Hostel Management - Student Creation'))
        self.stdout.write(self.style.SUCCESS('Password = Surname (with capital first letter)'))
        self.stdout.write(self.style.SUCCESS('=' * 70))

        # Create admin if requested
        if options['admin']:
            self.stdout.write('\n📌 Creating Admin/Superuser...')
            if User.objects.filter(username='admin').exists():
                self.stdout.write(self.style.WARNING('⚠️  Admin already exists'))
            else:
                User.objects.create_superuser(
                    username='admin',
                    email='admin@trinity.edu',
                    password='admin123456'
                )
                self.stdout.write(self.style.SUCCESS('✅ Admin created: admin / admin123456'))

        created_count = 0

        # Handle CSV file
        if options['csv']:
            created_count = self.handle_csv(options['csv'])

        # Handle single student
        elif options['name'] and options['matric']:
            created_count = self.handle_single_student(
                options['name'],
                options['matric'],
                options['gender'],
                options['level']
            )

        else:
            self.stdout.write('\n' + self.style.WARNING('⚠️  No input provided'))
            self.stdout.write('\nUsage Examples:')
            self.stdout.write('  1. Single student:')
            self.stdout.write('     python manage.py create_students_custom --name "John Doe" --matric STU001 --gender M --level 100')
            self.stdout.write('\n  2. From CSV file:')
            self.stdout.write('     python manage.py create_students_custom --csv students.csv')
            self.stdout.write('\n  3. With admin:')
            self.stdout.write('     python manage.py create_students_custom --admin --csv students.csv')
            return

        # Summary
        self.stdout.write('\n' + self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('✅ Student Creation Complete!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f'\n📊 Total Created: {created_count} student(s)')
        self.stdout.write('\n📝 Password Formula: Surname with capital first letter')
        self.stdout.write('   Example: "John Doe" → Password: "Doe"')
        self.stdout.write('           "Alice Smith" → Password: "Smith"')
        self.stdout.write('\n✨ Ready to use!\n')
