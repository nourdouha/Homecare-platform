from rest_framework import serializers
from appointment.models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'scheduled_time']

class AppointmentSolutionSerializer(serializers.Serializer):
    appointments = AppointmentSerializer(many=True)
