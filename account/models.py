from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
#%%

class AccountManager(BaseUserManager):
#  or not validate_email(email)
    # Must override create_user and create_superuser
    def create_user(self, email, password, first_name, last_name):
        if not email:
            raise ValueError("Users must have a valid email address")
        if not password:
            raise ValueError("Users must have a valid password")
        if not first_name:
            raise ValueError("Users must have a valid first_name")
        if not last_name:
            raise ValueError("Users must have a valid last_name")

        user = self.model(
            email=self.normalize_email(email),
            # password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email        = models.EmailField(verbose_name="email", max_length=60, unique=True)
    password     = models.CharField(verbose_name="password", max_length=100)
    date_joined  = models.DateTimeField(verbose_name="date", auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name   = models.CharField(verbose_name="first name", max_length=60, unique=False)
    last_name    = models.CharField(verbose_name="last name", max_length=60, unique=False)
    institution  = models.CharField(verbose_name="School/Company", max_length=60, unique=False)

    objects = AccountManager()

    # Whatever you want the user to login in with
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name',]

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


            
    

        
