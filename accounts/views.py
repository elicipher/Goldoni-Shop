from rest_framework.views import APIView 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status , generics , mixins
from .serializers import (
    SendOTPCodeSerializers ,
    VerifyOTPCodeSerializers,
    UserRegisterSerializers,
    AddressSerializers,
    ) 
from .models import OTPCode , User , Address
from rest_framework.throttling import AnonRateThrottle , UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated , AllowAny
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError

# Create your views here.

class SendOTPCodeAPIView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle , UserRateThrottle]
    @swagger_auto_schema(
            operation_summary = "ارسال کد یک بار مصرف به کاربر.",
            operation_description=
            """
            با ارسال شماره تلفن کد یکبار مصرف ساخته شده و به کاربر ارسال میشود.

            تعداد دفعات دریافت کد برای هر کاربر : ۱۰
            زمان منقضی شدن کد : ۲ دقیقه

            اعتبار سنجی :
            -شماره باید با ۰۹ شروع شود.
            -تعداد ارقام باید ۱۱ رقم باشد.

            """,
            responses={

            201: openapi.Response(
                description="OTP created",
                schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING , example="348912")
                    }
                ),
            ),
            400: "Bad Request",
            429: "Too Many Requests"

            },
            request_body=SendOTPCodeSerializers
    )

    def post(self , request) :
        serializer_data = SendOTPCodeSerializers(data=request.data)
        if serializer_data.is_valid():
            phone_number = serializer_data.validated_data["phone_number"]
            OTPCode.objects.filter(phone_number = phone_number).delete()
            otp_code = OTPCode.objects.create(phone_number = phone_number)
            code = otp_code.generate_otp()
            return Response({"code" : code} , status=status.HTTP_201_CREATED)

        return Response(serializer_data.errors , status=status.HTTP_400_BAD_REQUEST)

               

class VerifyOTPCodeAPIView(APIView):
 
    throttle_classes = [AnonRateThrottle , UserRateThrottle]
    permission_classes = [AllowAny]
    @swagger_auto_schema(
            operation_summary="اعتبار سنجی کد یکبار مصرف برای ورود یا ثبت نام",
            operation_description="""
            این ویو مقدار کد ارسال شده و شماره تلفن را میگیرید و در صورت درست بودن کد به کاربر پاسخ درست را میدهد.
            در صورتی که کد درست بوده باشد کاربر ورود یا وارد مرحله ثبت نام شده و درنهایت کد یکبار مصرف آن در دیتابیس حذف میشود.


            اگر کاربر ثبت شده/لاگین شده باشد :
            {
                "is_registered": true,
                "access": "...",
                "refresh": "..."
            }
           
           
            اگر کاربر  تازه وارد باشد :
            {
                "is_registered": false,
                "message": "لطفا اطلاعاتتان را پر کنید",
                "phone_number": "..."
            }
            و به صفحه رجیستر منتقل میشود جهت ثبت نهایی نام و شماره تلفن و دیگر اطلاعات کاربر در دیتابیس.

            """,
            request_body=VerifyOTPCodeSerializers,
            responses={
            200: VerifyOTPCodeSerializers(),
            400: "Bad Request",
            },

    )
    

    def post(self, request):
        serializer_data = VerifyOTPCodeSerializers(data=request.data)
        serializer_data.is_valid(raise_exception=True)

        phone_number = serializer_data.validated_data["phone_number"]

        user = User.objects.filter(phone_number = phone_number ).first()
        if user :
            refresh = RefreshToken.for_user(user)
            return Response({
                "is_registered":True,
                "access" : str(refresh.access_token),
                "refresh":str(refresh),
            }, status=status.HTTP_200_OK)
        
        else :
            return Response({
                "is_registered":False,
                "message":"لطفا اطلاعاتتان را پر کنید",
                "phone_number" : phone_number
            }, status=status.HTTP_200_OK)
                
            


class UserRegisterAPIView(mixins.CreateModelMixin , generics.GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializers
    @swagger_auto_schema(
            operation_summary="فرم ثبت نام کاربر",
            operation_description="""
              API ثبت‌نام کاربر جدید.

            این ویو اطلاعات کاربر را می‌گیرد، صحت آن‌ها را بررسی می‌کند و در صورت صحیح بودن، 
            یک حساب کاربری ایجاد می‌کند. سپس توکن‌های JWT (رفرش و اکسس) را در پاسخ برمی‌گرداند.

            اعتبارسنجی‌های مهم:
            - شماره تلفن باید 11 رقم و با «09» شروع شود.
            - کد ملی باید 10 رقم باشد.
            - رمز عبور باید شامل حروف کوچک، بزرگ و کاراکتر خاص باشد.
            - تاریخ تولد باید فرمت صحیح داشته باشد.
            - مختصات جغرافیایی (latitude و longitude) باید مقدار معتبر عددی باشند.


            """,
            request_body=UserRegisterSerializers,
            responses={
                201:UserRegisterSerializers(),
                400: "Bad Request",

            }



    )
    def post(self, request, *args, **kwargs):
            
            seri = self.serializer_class(data = request.data)
            seri.is_valid(raise_exception=True)
            user = seri.save()
            refresh = RefreshToken.for_user(user)
            serializer_data = seri.data

            serializer_data["token"] = {
                "is_registered":True,
                "refresh":str(refresh),
                "access":str(refresh.access_token)
            }

            return Response(serializer_data , status= status.HTTP_201_CREATED )


class UserProfileUpdateAPIView(generics.RetrieveUpdateAPIView):

    serializer_class = UserRegisterSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # فقط کاربر خودش
        return self.request.user
    
    @swagger_auto_schema(
        tags=["Profile Screen"],
        operation_summary="ویرایش پروفایل کاربر",
        operation_description="""
        این متد پروفایل کاربر لاگین‌شده را ویرایش می‌کند.
        
        - فقط فیلدهایی که ارسال می‌کنید آپدیت می‌شوند.
        - اگر بخشی نامعتبر باشد، پیام خطا و دلیل آن برمی‌گردد.
        - کاربر فقط می‌تواند اطلاعات خودش را ویرایش کند.
        """,
        request_body=UserRegisterSerializers,
        responses={
            200: UserRegisterSerializers(),
            400: "Validation Error",
            401: "Unauthorized",
           
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    @swagger_auto_schema(
        tags=["Profile Screen"],
        operation_summary="نمایش پروفایل کاربر",
        operation_description="پروفایل کاربر لاگین شده را برمیگرداند تا کاربر اطلاعات خود را ببیند.",
        responses = {
            200:UserRegisterSerializers(),
            401: "Unauthorized",

        }

    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):

        user = self.get_object()
        serializer = self.serializer_class(user , data = request.data ,partial = True )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status= status.HTTP_200_OK)

                    
                
class CheckAccessTokenApiView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            tags=["account"],
            operation_summary="بررسی اکسس توکن",
            operation_description="این ویو بررسی میکند که اکسس توکن منقضی شده است یا خیر اگر پاسخ ولید بود یعنی توکن هنوز سالم است و منقضی نشده است.",
            responses={
                200:"The Token is Valid",
                401:"The Token is expired",
            }
    )
    def get(self , request):
        return Response({"valid":True},status=status.HTTP_200_OK)


class MyAddressesGenericView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializers

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    @swagger_auto_schema(
            tags=["Profile Screen"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
            tags=["Profile Screen"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
            tags=["Profile Screen"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
            tags=["Profile Screen"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
            tags=["Profile Screen"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
            tags=["Profile Screen"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    
    

    

            

class LogOutAPIView(APIView):
    def post(self, request):
        
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"refresh": "لطفا توکن رفرش را ارسال کنید"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            BlacklistedToken.objects.filter(token__expires_at__lt=timezone.now()).delete()
            OutstandingToken.objects.filter(expires_at__lt=timezone.now()).delete()

        except TokenError:
            return Response(
                {"refresh": "توکن نامعتبر است"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
                    {"refresh": "شما با موفقیت از حساب کاربری خود خارج شدید"},
                    status=status.HTTP_205_RESET_CONTENT
            )
