from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendOTPCodeSerializers , VerifyOTPCodeSerializers
from .models import OTPCode
from rest_framework.throttling import AnonRateThrottle , UserRateThrottle
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

    def post(self, request):
        serializer_data = VerifyOTPCodeSerializers(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        if serializer_data.errors :
            if "phone_number" in serializer_data.errors :
                return Response(serializer_data.errors , status.HTTP_404_NOT_FOUND)
            
            return Response(serializer_data.errors , status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "کد صحیح است! ورود موفق."}, status=200)


        



                    
                
            


            


        

