from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self , phone_number ,full_name , password , **extra_fields):

        if not phone_number :
            raise ValueError("The user must be have phone number.")
        
        if not full_name :
            raise ValueError("The user must be have full name.")
        
        user = self.model(phone_number = phone_number , full_name = full_name ,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, full_name , phone_number ,  password  , **extra_fields):
        if not phone_number :
            raise ValueError("The user must be have phone number.")
        
        if not full_name :
            raise ValueError("The user must be have full name.")
        
        
        user = self.model(phone_number = phone_number , full_name = full_name , **extra_fields)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
