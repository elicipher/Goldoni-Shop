from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics , mixins
from .serializers import (
    SendOTPCodeSerializers ,
    VerifyOTPCodeSerializers,
    UserRegisterSerializers
    )
from .models import OTPCode , User
# from rest_framework.throttling import AnonRateThrottle , UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated , AllowAny
<<<<<<< HEAD
from drf_yasg.utils import swagger_auto_schema
=======
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi
>>>>>>> edb947b97584b34cbe74bc837c3a16415359efa5

# Create your views here.

class SendOTPCodeAPIView(APIView):

<<<<<<< HEAD
    This view accepts a POST request with a phone number, generates a new OTP code,
    and returns it in the response. If there is already an existing OTP for the
    same phone number, it will be deleted before generating a new one.

    Throttling:
        - Anonymous users: limited to 10 requests per hour
        - Authenticated users: limited to 10 requests per hour

    Request body (JSON):
        {
            "phone_number": "09123456789"
        }

    Response (JSON, status 201):
        {
            "code": "348912"
        }

    Validation:
        - The phone number must start with "09"
        - Only numeric characters are allowed


    Errors:
        - 400 Bad Request if the serializer validation fails
        - 429 Too Many Requests if throttling limit is exceeded
=======
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
>>>>>>> edb947b97584b34cbe74bc837c3a16415359efa5



    """

    # throttle_classes = [AnonRateThrottle , UserRateThrottle]

    @swagger_auto_schema(
        tags=['Auth Api'],
        request_body=SendOTPCodeSerializers,
        operation_description="ارسال شماره تلفن برای دریافت کد OTP جدید"
    )
    def post(self , request) :
        serializer_data = SendOTPCodeSerializers(data=request.data)
        if serializer_data.is_valid():
            phone_number = serializer_data.validated_data["phone_number"]
            OTPCode.objects.filter(phone_number = phone_number).delete()
            otp_code = OTPCode.objects.create(phone_number = phone_number)
            code = otp_code.generate_otp()
            return Response({"code" : code , "phone":phone_number} , status=status.HTTP_201_CREATED)

        return Response(serializer_data.errors , status=status.HTTP_400_BAD_REQUEST)



class VerifyOTPCodeAPIView(APIView):
<<<<<<< HEAD
    """
    API endpoint for verifying a One-Time Password (OTP) code sent to a user's phone number.

    This view accepts a POST request with a phone number and an OTP code. It validates
    the OTP code against the latest code stored in the database for that phone number.
    If the code is correct and not expired, it confirms successful verification and deletes
    the OTP record.

    Throttling:
        - Anonymous users: limited to 5 requests per day
        - Authenticated users: limited to 5 requests per day

    Request body (JSON):
        {
            "phone_number": "09123456789",
            "code": "348912"
        }

    Response (JSON, status 200):
        {
            "message": "کد صحیح است! ورود موفق."
        }

    Validation and errors:
        - 400 Bad Request if the serializer validation fails (wrong code, expired, or invalid phone number)
        - 404 Not Found if the phone number does not exist
        - 429 Too Many Requests if throttling limit is exceeded
    """
    # throttle_classes = [AnonRateThrottle , UserRateThrottle]
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        tags=['Auth Api'],
        request_body=VerifyOTPCodeSerializers,
        operation_description = "200 کدی که تو صفحه SendOTPCodeAPIView دادی رو اینجا میفرستی به همراه کدی که برات ارسال شد اگه شماره اشتباه بدی نمیتونی ورود کنی "
    )
=======
 
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
            200: "Verify OTP result",
            400: "Bad Request",
            },

    )
    
>>>>>>> edb947b97584b34cbe74bc837c3a16415359efa5

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

<<<<<<< HEAD
    This view allows clients to create a new user account by sending a POST request
    with the required user data. Upon successful registration, it returns the user
    data along with access and refresh tokens for authentication.

    """
    serializer_class = UserRegisterSerializers

    permission_classes = [AllowAny]
    @swagger_auto_schema(
        tags=['Auth Api'],
        request_body=UserRegisterSerializers,
    )

=======
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
                201:"The User Created",
                400: "Bad Request",

            }



    )
>>>>>>> edb947b97584b34cbe74bc837c3a16415359efa5
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
<<<<<<< HEAD
    """
    API view for retrieving and updating the authenticated user's profile.

    """
=======
>>>>>>> edb947b97584b34cbe74bc837c3a16415359efa5

    serializer_class = UserRegisterSerializers
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['Auth Api'],
    )
    def get_object(self):
        # فقط کاربر خودش
        return self.request.user
    
    @swagger_auto_schema(
        operation_summary="ویرایش پروفایل کاربر",
        operation_description="""
        این متد پروفایل کاربر لاگین‌شده را ویرایش می‌کند.
        
        - فقط فیلدهایی که ارسال می‌کنید آپدیت می‌شوند.
        - اگر بخشی نامعتبر باشد، پیام خطا و دلیل آن برمی‌گردد.
        - کاربر فقط می‌تواند اطلاعات خودش را ویرایش کند.
        """,
        request_body=UserRegisterSerializers,
        responses={
            200: "Profile updated successfully",
            400: "Validation Error",
            401: "Unauthorized",
           
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    @swagger_auto_schema(
            
        operation_summary="نمایش پروفایل کاربر",
        operation_description="پروفایل کاربر لاگین شده را برمیگرداند تا کاربر اطلاعات خود را ببیند.",
        responses = {
            200:"Ok",
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

<<<<<<< HEAD
=======
                    
                
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


>>>>>>> edb947b97584b34cbe74bc837c3a16415359efa5










