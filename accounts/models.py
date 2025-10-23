from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django_jalali.db import models as jmodels
from .managers import UserManager
# Create your models here.

class User(AbstractBaseUser):

    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=11 , unique= True)
    national_code = models.CharField(max_length=10)
    birthday_date = jmodels.jDateField(null=True , blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

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



class Location(models.Model):

    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user_location")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


    def __str__(self):

        return f"{self.name} ({self.latitude}, {self.longitude})"
