from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils import timezone
from datetime import timedelta
import random
from iranian_cities.fields import ProvinceField , CityField 
# Create your models here.

class User(AbstractBaseUser):

    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=500 , null = True )
    phone_number = models.CharField(max_length=11, unique=True , blank= False)
    national_code = models.CharField(max_length=10 , null= True , blank= False , unique= True)
    birthday_date = models.CharField(max_length=10 )

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    latitude = models.DecimalField(max_digits=9, decimal_places=6 , null=True , blank= False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6 , null=True , blank= False)

    last_login = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["full_name" , ]
    objects = UserManager()


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return f"{self.full_name} , {self.phone_number}"





class OTPCode(models.Model):

    phone_number = models.CharField(max_length=11, unique= True)
    code = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number

    def check_and_delete_expired(self):

        return timezone.now() > self.created + timedelta(minutes= 2)

    def generate_otp(self):

        self.code = str(random.randint(100000,999999))
        self.save()
        return self.code


class Address(models.Model):

    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="addresses",verbose_name="کاربر")
    province = ProvinceField(verbose_name="استان")
    city = CityField(verbose_name="شهر")
    postal_code = models.CharField(max_length=10,blank=True,null=True,verbose_name="کد پستی" )
    plaque = models.CharField( max_length=10,verbose_name="پلاک")
    address = models.CharField(max_length=500 , verbose_name="آدرس کامل ")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.province} - {self.city} - {self.plaque}"

