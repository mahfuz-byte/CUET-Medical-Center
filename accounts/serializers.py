from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'student_id', 'phone', 'is_active']
        read_only_fields = ['id', 'role', 'is_active']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for student self-registration."""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name', 'student_id', 'phone']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            student_id=validated_data.get('student_id'),
            phone=validated_data.get('phone'),
            role='student'
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']


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
