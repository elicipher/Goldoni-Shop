from rest_framework import serializers
from .models import OTPCode


class SendOTPCodeSerializers(serializers.Serializer):
    
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):

        if not value.startswith("09"):
            raise serializers.ValidationError("شماره تلفن نامعتبر است")
        
        if not value.isdigit():
            raise serializers.ValidationError("شماره تلفن باید فقط شامل عدد باشد.")
        
        if len(value) < 10 or len(value) > 11 :
            raise serializers.ValidationError("مقدار وارد شده شماره تلفن اشتباه می باشد")
        
        if not value.isdigit():
            raise serializers.ValidationError("شماره تلفن فقط می‌تواند عدد باشد.")
        
        return value
    

class VerifyOTPCodeSerializers(serializers.Serializer):
    code = serializers.CharField(max_length = 6)
    phone_number = serializers.CharField(max_length=11)

    def validate(self, data):
        phone_number = data.get("phone_number")
        code = data.get("code")

        try:
            otp_obj = OTPCode.objects.get(phone_number=phone_number)
        except OTPCode.DoesNotExist:
            raise serializers.ValidationError({"phone_number": "کد یافت نشد"})

        if otp_obj.check_and_delete_expired():
            otp_obj.delete()
            raise serializers.ValidationError({"code": "کد منقضی شده است."})

        if otp_obj.code != code:
            raise serializers.ValidationError({"code": "کد اشتباه است."})

        otp_obj.delete()

        return data

        


    