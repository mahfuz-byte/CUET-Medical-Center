#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuet_medical.settings')
sys.path.insert(0, '/d/My Downloads/IP Project/CUET-Medical-Center')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("Testing Email Configuration...")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD)}")

try:
    send_mail(
        'CUET Medical Center - Email Test',
        'If you receive this, your email configuration is working!',
        settings.EMAIL_HOST_USER,
        ['u2204092@student.cuet.ac.bd'],
        fail_silently=False,
    )
    print("\n✅ Email sent successfully!")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
