from django.db import models
from django.contrib.auth.models import AbstractUser


# here we create the Custom User model used to add new users for the platform
class User(AbstractUser):
    email= models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10 ,null=True)
