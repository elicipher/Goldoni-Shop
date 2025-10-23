from django.urls import path
from . import views


urlpatterns = [
    path("send-otp-code/" , views.SendOTPCodeAPIView.as_view() ),
    path("verify_otp_code/" , views.VerifyOTPCodeAPIView.as_view() ),
]