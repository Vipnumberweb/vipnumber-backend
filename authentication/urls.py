from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    ResendOTPView,
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserDetailsView.as_view(), name='user_details'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
]
