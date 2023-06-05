from django.urls import path , include
from .views import CustomRegisterViewPatient, MedicaleFileViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'MedicalFile', MedicaleFileViewSet)

urlpatterns = [
    path('register/', CustomRegisterViewPatient.as_view(), name='register_patient'),
    path('api/', include(router.urls)),
]