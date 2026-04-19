import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuet_medical.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create Admin User
admin_email = 'admin_new@example.com'
admin_password = 'password123'
if not User.objects.filter(email=admin_email).exists():
    admin = User.objects.create_superuser(
        email=admin_email,
        password=admin_password,
        first_name='Admin',
        last_name='User',
        role='admin',
        password_plaintext=admin_password,
    )
    print(f"Created Admin: {admin_email} / {admin_password}")
else:
    admin = User.objects.get(email=admin_email)
    admin.set_password(admin_password)
    admin.password_plaintext = admin_password
    admin.role = 'admin'
    admin.is_active = True
    admin.save(update_fields=['password', 'password_plaintext', 'role', 'is_active'])
    print(f"Updated Admin credentials: {admin_email} / {admin_password}")
    print(f"Admin {admin_email} already exists")

# Create Doctor User
doctor_email = 'doctor_new@example.com'
doctor_password = 'password123'
if not User.objects.filter(email=doctor_email).exists():
    doctor = User.objects.create_user(
        email=doctor_email,
        password=doctor_password,
        first_name='Doctor',
        last_name='Who',
        role='doctor',
        password_plaintext=doctor_password,
    )
    print(f"Created Doctor: {doctor_email} / {doctor_password}")
else:
    doctor = User.objects.get(email=doctor_email)
    doctor.set_password(doctor_password)
    doctor.password_plaintext = doctor_password
    doctor.role = 'doctor'
    doctor.is_active = True
    doctor.save(update_fields=['password', 'password_plaintext', 'role', 'is_active'])
    print(f"Updated Doctor credentials: {doctor_email} / {doctor_password}")
    print(f"Doctor {doctor_email} already exists")

# Create Student User just in case
student_email = 'u2204093@student.cuet.ac.bd'
student_password = '1234'
student_id_from_email = '2204093'
legacy_student_email = 'student_new@student.cuet.ac.bd'

# Migrate legacy seeded student account to the new required email format if needed.
if User.objects.filter(email=legacy_student_email).exists() and not User.objects.filter(email=student_email).exists():
    student = User.objects.get(email=legacy_student_email)
    student.email = student_email
    student.student_id = student_id_from_email
    student.set_password(student_password)
    student.password_plaintext = student_password
    student.role = 'student'
    student.is_active = True
    student.save(update_fields=['email', 'student_id', 'password', 'password_plaintext', 'role', 'is_active'])
    print(f"Migrated Student credentials: {legacy_student_email} -> {student_email} / {student_password}")
elif not User.objects.filter(email=student_email).exists():
    student = User.objects.create_user(
        email=student_email,
        password=student_password,
        first_name='Student',
        last_name='One',
        role='student',
        student_id=student_id_from_email,
        password_plaintext=student_password,
    )
    print(f"Created Student: {student_email} / {student_password}")
else:
    student = User.objects.get(email=student_email)
    student.set_password(student_password)
    student.password_plaintext = student_password
    student.role = 'student'
    student.student_id = student_id_from_email
    student.is_active = True
    student.save(update_fields=['password', 'password_plaintext', 'role', 'student_id', 'is_active'])
    print(f"Updated Student credentials: {student_email} / {student_password}")
    print(f"Student {student_email} already exists")
