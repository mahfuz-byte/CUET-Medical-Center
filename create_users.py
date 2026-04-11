import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuet_medical.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create Admin User
admin_email = 'admin@example.com'
admin_password = 'admin123'
if not User.objects.filter(email=admin_email).exists():
    admin = User.objects.create_superuser(
        email=admin_email,
        password=admin_password,
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    print(f"Created Admin: {admin_email} / {admin_password}")
else:
    print(f"Admin {admin_email} already exists")

# Create Doctor User
doctor_email = 'doctor@example.com'
doctor_password = 'doctor123'
if not User.objects.filter(email=doctor_email).exists():
    doctor = User.objects.create_user(
        email=doctor_email,
        password=doctor_password,
        first_name='Doctor',
        last_name='Who',
        role='doctor'
    )
    print(f"Created Doctor: {doctor_email} / {doctor_password}")
else:
    print(f"Doctor {doctor_email} already exists")

# Create Student User just in case
student_email = 'student@example.com'
student_password = 'student123'
if not User.objects.filter(email=student_email).exists():
    student = User.objects.create_user(
        email=student_email,
        password=student_password,
        first_name='Student',
        last_name='One',
        role='student',
        student_id='STU001'
    )
    print(f"Created Student: {student_email} / {student_password}")
else:
    print(f"Student {student_email} already exists")
