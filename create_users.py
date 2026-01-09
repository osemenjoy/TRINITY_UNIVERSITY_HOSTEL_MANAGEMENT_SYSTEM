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
print("Created male student: John Doe (TRN2024001)")

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
    level='200'
)
print("Created female student: Amy Jones (TRN2024002)")

print("\nTest users created successfully!")
print("Student 1 - Username: jdoe, Password: password123")
print("Student 2 - Username: ajones, Password: password123")
