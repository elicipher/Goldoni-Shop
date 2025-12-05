from rest_framework import serializers
from .models import OTPCode , User , Address



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
            raise serializers.ValidationError({"message": "کد یافت نشد"})

        if otp_obj.check_and_delete_expired():
            otp_obj.delete()
            raise serializers.ValidationError({"message": "کد منقضی شده است."})

        if otp_obj.code != code:
            raise serializers.ValidationError({"message": "کد اشتباه است."})

        otp_obj.delete()

        return data


        
class UserRegisterSerializers(serializers.ModelSerializer):
    address = serializers.CharField(required = True)
    birthday_date = serializers.DateField(required = True)
    latitude = serializers.DecimalField(required = True  , max_digits= 9  , decimal_places= 6)
    longitude = serializers.DecimalField(required = True , max_digits= 9  , decimal_places= 6)



    class Meta:
        model = User
        exclude = ("is_active","is_admin","is_superuser",)

    def validate_phone_number(self, value ):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("شماره تلفن باید فقط شامل ۱۱ رقم باشد.")
        if not value.startswith("09") : 
            raise serializers.ValidationError("شماره تلفن نامعتبر است")
        return value
    
    def validate_national_code(self, value):
        if len(value) != 10  or not value.isdigit() :
            raise serializers.ValidationError("کد ملی باید شامل ۱۰ رقم باشد")
        return value
    
 

class AddressSerializers(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"

    



