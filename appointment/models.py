from django.db import models
from datetime import date
from doctor.models import Doctor
from patient.models import Patient


class Appointment(models.Model):
    date =models.DateField()
    
    patient= models.ForeignKey(Patient,  on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    address = models.CharField(max_length= 255, null= True)

    def __str__ (self):
        return self.patient.user.full_name
    

class Todayschedule:
    @classmethod
    def get_appointments(cls, doctor_id):
        today = date.today()
        return Appointment.objects.filter(date=today, doctor_id=doctor_id)
    

class Report(models.Model):
    patient= models.ForeignKey(Patient,  on_delete=models.CASCADE)
    Appointment = models.ForeignKey(Appointment,  on_delete=models.CASCADE)
    Appointment_reason = models.CharField(max_length=255, null= True)
    date = models.DateField(null=True)
    report_file = models.FileField(null=True)
    def __str__ (self):
        return Patient.user.full_name
