from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics , mixins
from .serializers import (
    SendOTPCodeSerializers ,
    VerifyOTPCodeSerializers,
    UserRegisterSerializers
    ) 
from .models import OTPCode , User
from rest_framework.throttling import AnonRateThrottle , UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated , AllowAny
# Create your views here.

class SendOTPCodeAPIView(APIView):
    """
    API endpoint for sending an OTP (One-Time Password) code to a user's phone number.

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
    
    
    
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle , UserRateThrottle]

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
    throttle_classes = [AnonRateThrottle , UserRateThrottle]
    permission_classes = [AllowAny]
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
    """
    API view for registering a new user and returning JWT tokens.

    This view allows clients to create a new user account by sending a POST request
    with the required user data. Upon successful registration, it returns the user
    data along with access and refresh tokens for authentication.

    Attributes:
        serializer_class (UserRegisterSerializers): 
            The serializer class used to validate input data and create the user.

    Methods:
        post(request, *args, **kwargs):
            Handles POST requests to register a new user.

            Steps performed:
            1. Instantiate the serializer with request data.
            2. Validate the input data. If invalid, raises an exception and returns errors.
            3. Save the validated data to create a new User instance.
            4. Generate JWT refresh and access tokens for the new user.
            5. Add the tokens to the serialized user data under the "Token" key.
            6. Return a Response containing the user data and tokens with HTTP 201 status.

    Request Body:
        The request must include all required fields defined in UserRegisterSerializers,
        for example:
        {
            "full_name": "Elmira",
            "phone_number": "09123456789",
            "national_code": "2345678910",
            "birthday_date": "2025-08-05",
            "password": "Elmira123@",
            "address": "Tehran",
            "latitude": "11.000000",
            "longitude": "789.000000",

        }

    Response:
        On success (HTTP 201):
        {
            "full_name": "Elmira",
            "phone_number": "09123456789",
            "national_code": "2345678910",
            "birthday_date": "2025-08-05",
            ...
            "Token": {
                "login": False,
                "refresh": "<refresh_token_here>",
                "access": "<access_token_here>"
            }
        }

        On validation error (HTTP 400):
        {
            "phone_number": ["شماره تلفن باید فقط شامل ۱۱ رقم باشد."],
            "national_code": ["کد ملی باید ۱۰ رقم باشد."],
            ...
        }
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializers
    def post(self, request, *args, **kwargs):
            
            seri = self.serializer_class(data = request.data)
            seri.is_valid(raise_exception=True)
            user = seri.save()
            refresh = RefreshToken.for_user(user)
            serializer_data = seri.data

            serializer_data["token"] = {
                "is_registered":False,
                "refresh":str(refresh),
                "access":str(refresh.access_token)
            }

            return Response(serializer_data , status= status.HTTP_201_CREATED )


class UserProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the authenticated user's profile.

    Permissions:
        - Only authenticated users can access this view.

    Methods:
        GET:
            - Retrieve the current authenticated user's profile.
            - Returns all fields of the user.

        PUT / PATCH:
            - Update the current authenticated user's profile.
            - `partial=True` allows partial updates (PATCH), but validation
              is still applied to provided fields.
            - If any field violates serializer validation rules (e.g., required
              fields are empty, phone number format invalid), a 400 response
              with details is returned.

    Usage:
        - The view automatically uses `request.user` as the object to update.
        - No need to provide a user ID in the URL; each user can only update
          their own profile.
    """

    serializer_class = UserRegisterSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # فقط کاربر خودش
        return self.request.user
    def update(self, request, *args, **kwargs):

        user = self.get_object()
        serializer = self.serializer_class(user , data = request.data ,partial = True )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status= status.HTTP_200_OK)

                    
                
            


            


        

