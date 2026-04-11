from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import OTP
from django.utils import timezone

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'role', 'student_id', 'phone', 'is_active']
        read_only_fields = ['id', 'is_active']


class SendOTPSerializer(serializers.Serializer):
    """Serializer for sending OTP to email."""
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=['student', 'doctor', 'admin'])

    def validate(self, attrs):
        email = attrs.get('email')
        role = attrs.get('role')
        
        # Validate email domain based on role
        if role == 'student':
            if not email.endswith('@student.cuet.ac.bd'):
                raise serializers.ValidationError({'error': 'Students must use @student.cuet.ac.bd email'})
        else:  # doctor or admin
            if not email.endswith('@cuet.ac.bd') or email.endswith('@student.cuet.ac.bd'):
                raise serializers.ValidationError({'error': 'Doctors and Admins must use @cuet.ac.bd email'})
        
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

        attrs['otp'] = otp
        return attrs

    def create(self, validated_data):
        otp = validated_data.pop('otp')
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            password_plaintext=validated_data['password'],
            role=otp.role,
            is_active=True
        )
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

        # Check plaintext password
        if user.password_plaintext != password:
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
