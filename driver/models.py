from django.db import models
from user.models import User
from doctor.models import Doctor
# Create your models here.


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE ,null=True) #no need to associate the driver to a ambulace

class Ambulance(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
