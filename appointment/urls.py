from django.urls import path, include
from rest_framework import routers
from .views import AppointmentViewSet, ReportViewSet

router = routers.DefaultRouter()
router.register(r'appointment', AppointmentViewSet)
router.register(r'report', ReportViewSet)

urlpatterns = [
    # Other URL patterns
    path('api/', include(router.urls)),
]
