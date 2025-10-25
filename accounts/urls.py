from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("send-otp-code/" , views.SendOTPCodeAPIView.as_view() ),
    path("verify_otp_code/" , views.VerifyOTPCodeAPIView.as_view() ),
    path("register/" , views.UserRegisterAPIView.as_view() ),
    path("profile/" , views.UserProfileUpdateAPIView.as_view() ),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]