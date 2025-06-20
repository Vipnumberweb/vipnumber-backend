from django.urls import path 
from .views import (
    RegisterView,
    # VerifyOTPView,      ❌ Remove or comment this
    # ResendOTPView,      ❌ Remove or comment this
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),  ❌ comment this
    # path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),  ❌ comment this
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserDetailsView.as_view(), name='user_details'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
]
