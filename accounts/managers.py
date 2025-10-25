from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, password=None, **extra_fields):

        required_fields = ["phone_number", "full_name", "national_code", "birthday_date" , "latitude" , "longitude"]

        for field in required_fields:
            if not extra_fields.get(field):
                raise ValueError(f"{field.replace('_', ' ').title()} is required for cre users.")

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, full_name , phone_number ,  password  ):
        if not phone_number :
            raise ValueError("The user must be have phone number.")
        
        if not full_name :
            raise ValueError("The user must be have full name.")
        
        
        
        
        user = self.model(phone_number = phone_number , full_name = full_name  )
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
