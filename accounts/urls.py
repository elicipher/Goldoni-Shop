from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'my-addresses', views.MyAddressesGenericView, basename='my-addresses')
urlpatterns = [
    path("send-otp-code/" , views.SendOTPCodeAPIView.as_view() ),
    path("verify_otp_code/" , views.VerifyOTPCodeAPIView.as_view() ),
    path("register/" , views.UserRegisterAPIView.as_view() ),
    path("profile/" , views.UserProfileUpdateAPIView.as_view() ),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/check/access_token/",views.CheckAccessTokenApiView.as_view(), name="token_access"),
    path("logout/",views.LogOutAPIView.as_view(),name="logout")
    
]+ router.urls