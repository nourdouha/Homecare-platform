from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, Medical_file
#from django.contrib.auth.models import Group

class CustomRegisterSerializerPatient(RegisterSerializer):
    full_name = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=10, required=False)
    birthday = serializers.DateField(required=False)
    address = serializers.CharField(max_length=255, required=False)
    #----
    address_latitude = serializers.FloatField(required=False)
    address_longitude = serializers.FloatField(required=False)
    picture = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['full_name'] = self.validated_data['phone_number']
        data['phone_number'] = self.validated_data['full_name']
        data['birthday'] = self.validated_data['birthday']
        data['address'] = self.validated_data['address']
        #---
        data['address_latitude'] = self.validated_data['address_latitude']
        data['address_longitude'] = self.validated_data['address_longitude']
        data['picture'] = self.validated_data['picture']
        return data

    def save(self, request):
        # Create a new user  
        user = super().save(request)
        user.full_name = self.validated_data['full_name']
        user.phone_number = self.validated_data['phone_number']
        user.save()
        
        # Create a patient object and assign the user
        patient_obj = Patient.objects.create(user=user)
        patient_obj.birthday = self.validated_data.get('birthday')
        patient_obj.address = self.validated_data.get('address')

        patient_obj.address_latitude = self.validated_data.get('address_latitude')
        patient_obj.address_longitude = self.validated_data.get('address_longitude')
        patient_obj.picture = self.validated_data.get('picture')
        patient_obj.save()


        return user
    

class MedicalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_file
        fields = '__all__'
