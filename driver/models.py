from django.db import models
from user.models import User
from doctor.models import Doctor
from appointment.models import Appointment
# Create your models here.


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE ,null=True) #no need to associate the driver to a ambulace

class Ambulance(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

class OptimizedRoute(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    appointment1 = models.ForeignKey()