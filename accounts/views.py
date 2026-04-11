from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserSerializer, SendOTPSerializer, VerifyOTPSerializer, 
    SignupSerializer, LoginSerializer, CustomTokenObtainPairSerializer
)
from .models import OTP

User = get_user_model()


class SendOTPView(generics.GenericAPIView):
    """Send OTP to the provided email."""
    serializer_class = SendOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        role = serializer.validated_data['role']

        # Create OTP
        otp_obj = OTP.create_otp(email, role)

        # Send OTP via email
        try:
            subject = 'Your OTP for CUET Medical Center Registration'
            message = f'''
Welcome to CUET Medical Center!

Your One-Time Password (OTP) for registration is: {otp_obj.otp_code}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  This OTP will expire in 5 minutes
Role: {role.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Instructions:
1. Enter this OTP in the signup form
2. Complete your profile registration
3. Start using CUET Medical Center

⚠️  Did not request this? Please ignore this email or contact our support team.

Best regards,
CUET Campus Medical Center
Pahartoli, Raozan, Chattogram
Phone: +880-31-714946
Email: medical@cuet.edu

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
© 2026 CUET Medical Center. All rights reserved.
            '''
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response(
                {'message': f'OTP sent to {email}', 'email': email},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to send OTP: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyOTPView(generics.GenericAPIView):
    """Verify the OTP provided by the user."""
    serializer_class = VerifyOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {'message': 'OTP verified successfully', 'verified': True},
            status=status.HTTP_200_OK
        )


class SignupView(generics.GenericAPIView):
    """Complete user registration after OTP verification."""
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                'message': 'Registration successful! Please login.',
                'user': UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.GenericAPIView):
    """Login user with email and plaintext password."""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            from .serializers import UserProfileUpdateSerializer
            return UserProfileUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """Delete user account"""
        user = self.get_object()
        user_email = user.email
        user.delete()
        return Response(
            {'message': f'Account {user_email} has been deleted successfully'},
            status=status.HTTP_200_OK
        )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
