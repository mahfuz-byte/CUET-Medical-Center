from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SendOTPView, VerifyOTPView, SignupView, LoginView,
    RegisterView, ProfileView
)

urlpatterns = [
    # New OTP-based auth flow
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    
    # Legacy endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ProfileView.as_view(), name='profile'),
]
