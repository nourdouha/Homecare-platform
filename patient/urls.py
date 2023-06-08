from django.urls import path , include
from .views import CustomRegisterViewPatient, MedicalFileAPIView
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('register/', CustomRegisterViewPatient.as_view(), name='register_patient'),
    path('api/', include(router.urls)),
    path('medicalfile', MedicalFileAPIView.as_view(), name='medicalfile')
]