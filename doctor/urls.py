from django.urls import path , include
from .views import CustomRegisterViewDoctor,CustomRegisterSerializerNurse

urlpatterns = [
    path('doctorregister/', CustomRegisterViewDoctor.as_view(), name='register_doctor'),
    path('nurseregister/', CustomRegisterViewDoctor.as_view(), name='register_nurse'),
]