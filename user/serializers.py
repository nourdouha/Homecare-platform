from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=10, required=False)
    

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['phone_number'] = self.validated_data['full_name']
        data['full_name'] = self.validated_data['phone_number']
        return data

    def save(self, request):
        user = super().save(request)
        user.full_name = self.validated_data['full_name']
        user.phone_number = self.validated_data['phone_number']
        user.save()
        return user
    

