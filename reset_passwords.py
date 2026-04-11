import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuet_medical.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Define credentials
credentials = {
    'admin@example.com': 'admin123',
    'doctor@example.com': 'doctor123',
    'student@example.com': 'student123',
}

for email, password in credentials.items():
    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        print(f"✓ Reset password for {email}")
    except User.DoesNotExist:
        print(f"✗ User {email} not found")

print("\nPassword reset complete!")
