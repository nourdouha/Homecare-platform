from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth.models import Group




# here we create the Custom User model used to add new users for the platform
class User(AbstractUser):
    email= models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10 ,null=True)


# creating groups "patient" , "doctor", "nurse", "driver" for each app user 

class patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    #----------------
    birthday =  models.DateField(null=True)


class doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=255 )
    #---------
    address = models.CharField(max_length=255, null=True)
    birthday =  models.DateField()

class nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    birthday =  models.DateField(null=True)

class driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    birthday =  models.DateField(null=True)