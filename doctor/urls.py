from django.urls import path , include
from .views import CustomRegisterViewDoctor,CustomRegisterSerializerNurse, get_doctors, get_doctorss

urlpatterns = [
    path('doctorregister/', CustomRegisterViewDoctor.as_view(), name='register_doctor'),
    path('nurseregister/', CustomRegisterViewDoctor.as_view(), name='register_nurse'),
    path('doctorlist',get_doctorss, name='doctorlist')
]