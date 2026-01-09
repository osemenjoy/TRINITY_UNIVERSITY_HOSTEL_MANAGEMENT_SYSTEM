from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hostels.models import StudentProfile


class Command(BaseCommand):
    help = 'Create test student accounts and admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of students to create (default: 10)'
        )
        parser.add_argument(
            '--admin',
            action='store_true',
            help='Create admin/superuser'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='studentpass123',
            help='Password for created accounts'
        )

    def handle(self, *args, **options):
        count = options['count']
        create_admin = options['admin']
        password = options['password']

        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Creating Users for Trinity Hostel Management'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Create admin if requested
        if create_admin:
            self.stdout.write('\n📌 Creating Admin/Superuser...')
            if User.objects.filter(username='admin').exists():
                self.stdout.write(self.style.WARNING('⚠️  Admin user already exists'))
            else:
                User.objects.create_superuser(
                    username='admin',
                    email='admin@trinity.edu',
                    password='admin123456'
                )
                self.stdout.write(self.style.SUCCESS('✅ Admin created: admin / admin123456'))

        # Create students
        self.stdout.write(f'\n👥 Creating {count} test students...')
        genders = ['M', 'F']
        levels = ['100', '200', '300', '400']
        created_count = 0

        for i in range(1, count + 1):
            username = f'stu{i:03d}'
            matric_no = f'STU{i:03d}'

            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'⚠️  {username} already exists, skipping'))
                continue

            try:
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@trinity.edu',
                    password=password
                )

                StudentProfile.objects.create(
                    user=user,
                    matric_no=matric_no,
                    gender=genders[i % 2],
                    level=levels[i % 4]
                )

                self.stdout.write(
                    self.style.SUCCESS(f'✅ {username} ({matric_no}) - Level {levels[i % 4]}')
                )
                created_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error creating {username}: {str(e)}')
                )

        # Summary
        self.stdout.write('\n' + self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ User Creation Complete!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        self.stdout.write('\n📝 Login Credentials:')
        self.stdout.write(f'   Admin: admin / admin123456')
        self.stdout.write(f'   Students: stu001-stu{created_count:03d} / {password}')
        
        self.stdout.write('\n🔗 Login URLs:')
        self.stdout.write('   Admin Panel: /admin/')
        self.stdout.write('   Student Login: /accounts/login/')
        
        self.stdout.write(self.style.SUCCESS('\n✨ Ready to use!\n'))
