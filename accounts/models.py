from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta
import random
import re


STUDENT_EMAIL_REGEX = re.compile(r'^u(\d{7})@student\.cuet\.ac\.bd$', re.IGNORECASE)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    BLOOD_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    username = None
    first_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    password_plaintext = models.CharField(max_length=255, blank=True, null=True)  # Plaintext password storage
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    # Student-specific fields
    student_id = models.CharField(max_length=20, blank=True, null=True)
    dept = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_CHOICES, blank=True, null=True)
    
    # Doctor-specific fields
    specialization = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    
    # Admin-specific fields
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Common fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Keep student_id synchronized with CUET student email format.
        if self.role == 'student' and self.email:
            match = STUDENT_EMAIL_REGEX.match(self.email.strip())
            if match:
                self.student_id = match.group(1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class OTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    role = models.CharField(max_length=10, choices=User.ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    @staticmethod
    def generate_otp():
        """Generate a 5-digit numeric OTP"""
        return str(random.randint(10000, 99999))

    @staticmethod
    def create_otp(email, role):
        """Create and return a new OTP"""
        otp_code = OTP.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=5)
        otp = OTP.objects.create(
            email=email,
            otp_code=otp_code,
            role=role,
            expires_at=expires_at
        )
        return otp

    def is_valid(self):
        """Check if OTP is still valid and not used"""
        return not self.is_used and timezone.now() < self.expires_at

    def mark_used(self):
        """Mark OTP as used"""
        self.is_used = True
        self.save()

    def __str__(self):
        return f"{self.email} - {self.role}"
