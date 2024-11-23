from typing import Optional

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class UserModelManager(BaseUserManager):
    def create_user(self,
                    email: str,
                    first_name: str,
                    last_name: str,
                    password: Optional[str] = None,
                    **extra_fields):
        
        if not email:
            raise ValidationError("Email Address must not be empty ...")
        
        if not first_name:
            raise ValidationError("First Name must not be empty ...")
        
        if not last_name:
            raise ValidationError("Last Name must not be empty ...")
        
        user = self.model(email=email, first_name=first_name, 
                          last_name=last_name, **extra_fields)
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self.db)
        return user
    
    def create_superuser(self,
                         email: str,
                         first_name: str,
                         last_name: str,
                         password: str,
                         **extra_fields):
        
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True

        return self.create_user(email=email, first_name=first_name, 
                                last_name=last_name, **extra_fields)
