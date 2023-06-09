from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from doctor.models import MedicalCenter, Doctor, nurse, optimizedRoute
from patient.models import Patient
from appointment.models import Appointment, Report

#to make the admin have the field of email in adding users 
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","email","full_name","phone_number","password1", "password2"),
            },
        ),
    )

#to make the admin responsable for those models
admin.site.register(MedicalCenter)
admin.site.register(Doctor)
admin.site.register(nurse)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Report)
admin.site.register(optimizedRoute)