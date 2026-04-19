from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import OTP
from django.utils import timezone
import re

User = get_user_model()
STUDENT_EMAIL_REGEX = re.compile(r'^u(\d{7})@student\.cuet\.ac\.bd$', re.IGNORECASE)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'role', 'phone', 'is_active',
            # Student fields
            'student_id', 'dept', 'age', 'blood_group',
            # Doctor fields
            'specialization', 'qualification', 'license_number', 'experience',
            # Admin fields
            'designation', 'department', 'employee_id'
        ]
        read_only_fields = ['id', 'email', 'role', 'is_active']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'phone',
            # Student fields
            'student_id', 'dept', 'age', 'blood_group',
            # Doctor fields
            'specialization', 'qualification', 'license_number', 'experience',
            # Admin fields
            'designation', 'department', 'employee_id'
        ]
        read_only_fields = ['student_id']  # Make student_id read-only


class SendOTPSerializer(serializers.Serializer):
    """Serializer for sending OTP to email."""
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=['student', 'doctor', 'admin'])

    def validate(self, attrs):
        email = attrs.get('email')
        role = attrs.get('role')
        
        # Validate email domain based on role
        if role == 'student':
            if not STUDENT_EMAIL_REGEX.match(email):
                raise serializers.ValidationError({'error': 'Student email must follow uXXXXXXX@student.cuet.ac.bd format'})
        # Doctors and Admins can use any email address
        
        # Check if user with this email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email already registered'})
        
        return attrs


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer for verifying OTP."""
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6, min_length=5)

    def validate(self, attrs):
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')

        try:
            otp = OTP.objects.filter(email=email, otp_code=otp_code).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid OTP'})

        if not otp.is_valid():
            raise serializers.ValidationError({'error': 'OTP has expired or already used'})

        attrs['otp'] = otp
        return attrs


class SignupSerializer(serializers.Serializer):
    """Serializer for user signup after OTP verification."""
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=255, write_only=True)
    otp_code = serializers.CharField(max_length=6, min_length=5)

    def validate(self, attrs):
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')

        try:
            otp = OTP.objects.filter(email=email, otp_code=otp_code).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid OTP'})

        if not otp.is_valid():
            raise serializers.ValidationError({'error': 'OTP has expired or already used'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email already registered'})

        # Enforce student email format and derive student_id from it.
        if otp.role == 'student':
            match = STUDENT_EMAIL_REGEX.match(email)
            if not match:
                raise serializers.ValidationError({'error': 'Student email must follow uXXXXXXX@student.cuet.ac.bd format'})
            attrs['student_id'] = match.group(1)

        attrs['otp'] = otp
        return attrs

    def create(self, validated_data):
        otp = validated_data.pop('otp')
        student_id = validated_data.pop('student_id', None)
        raw_password = validated_data.pop('password')

        extra_fields = {}
        if otp.role == 'student' and student_id:
            extra_fields['student_id'] = student_id

        user = User.objects.create_user(
            email=validated_data['email'],
            password=raw_password,
            first_name=validated_data['first_name'],
            role=otp.role,
            is_active=True,
            **extra_fields,
        )
        # Keep backward compatibility with existing login flow.
        user.password_plaintext = raw_password
        user.save(update_fields=['password_plaintext'])
        otp.mark_used()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login using email and plaintext password."""
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid credentials'})

        if not user.is_active:
            raise serializers.ValidationError({'error': 'User account is disabled'})

        # Support both legacy plaintext field and Django hashed password.
        is_plaintext_match = user.password_plaintext == password
        is_hashed_match = user.check_password(password)
        if not (is_plaintext_match or is_hashed_match):
            raise serializers.ValidationError({'error': 'Invalid credentials'})

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to allow login with email instead of username."""
    
    username_field = User.USERNAME_FIELD
    
    email = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        # Map email to the username_field
        authenticate_kwargs = {
            self.username_field: attrs.get('email'),
            'password': attrs.get('password'),
        }
        
        try:
            authenticate_user = User.objects.get(email=attrs.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})
        
        if not authenticate_user.is_active:
            raise serializers.ValidationError({'detail': 'User account is disabled.'})
        
        if not authenticate_user.check_password(attrs.get('password')):
            raise serializers.ValidationError({'detail': 'No active account found with the given credentials'})
        
        refresh = self.get_token(authenticate_user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        data['user'] = UserSerializer(authenticate_user).data
        return data
