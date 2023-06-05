from django.db import models
from user.models import User

class Patient (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True) #to have doctors with same address
    birthday =  models.DateField(null =True) 
    address_latitude = models.FloatField(null=True)
    address_longitude = models.FloatField(null=True)
    picture = models.ImageField(null=True)
    
    
    def __str__ (self):
        return self.user.full_name
    

class Medical_file (models.Model):
    Patient = models.ForeignKey(Patient , null=True, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=10 , null=True)
    disease = models.CharField(max_length=255 , null= True)
    file = models.FileField()