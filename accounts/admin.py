from django.contrib import admin
from .models import User , OTPCode,Address
# Register your models here.
admin.site.register(User)
admin.site.register(OTPCode)
admin.site.register(Address)