from django.db import models
from user.models import User





class optimizedRoute(models.Model):
    driver = models.CharField(max_length=255)
    date = models.DateField()
    appointment1 = models.CharField(max_length=255)
    appointment2 = models.CharField(max_length=255)
    appointment3 = models.CharField(max_length=255)
    appointment4 = models.CharField(max_length=255)
    def __str__ (self):
        return self.driver

#@admin
class MedicalCenter(models.Model):
    medical_center =models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__ (self):
        return self.medical_center


#add api 
class Doctor (models.Model):
    speciality = models.CharField(max_length=255, null=True) #to show for the patient 

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True) #to be in patient's available doctors list
    birthday =  models.DateField(null =True) 
    picture = models.ImageField(null=True)

    #@admin
    MedicalCenter = models.ForeignKey(MedicalCenter,on_delete=models.CASCADE, null=True) # for the driver

    WORK_TIME_CHOICES = (
        ('morning', 'Morning'),
        ('evening', 'Evening'),
    ) 
    work_time = models.CharField(max_length=7, choices=WORK_TIME_CHOICES, null=True) #will be set by admin for organizing appointments
    def __str__ (self):
        return self.user.full_name
    

# add api 
class nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    birthday =  models.DateField(null=True)
    #@admin
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE, null=True) #for MedicalCenter , WorkTime, address
    
    def __str__ (self):
        return self.user.full_name





