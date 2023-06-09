from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Doctor, nurse
from django.contrib.auth.models import Group

class CustomRegisterSerializerDoctor(RegisterSerializer):
    full_name = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=10, required=False)
    speciality = serializers.CharField(max_length= 255, required =False)
    birthday = serializers.DateField(required=False)
    address = serializers.CharField(max_length=255, required=False)
    picture = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['phone_number'] = self.validated_data['full_name']
        data['full_name'] = self.validated_data['phone_number']
        data['speciality'] = self.validated_data['speciality']
        data['birthday'] = self.validated_data['birthday']
        data['address'] = self.validated_data['address']
        data['picture'] = self.validated_data['picture']
        return data

    def save(self, request):
        #create a user and save it 
        user = super().save(request)
        user.full_name = self.validated_data['full_name']
        user.phone_number = self.validated_data['phone_number']
        user.save()
        
        # Create a doctor object and assign the user
        doctor_obj = Doctor.objects.create(user=user)
        doctor_obj.speciality = self.validated_data.get('speciality')
        doctor_obj.birthday = self.validated_data.get('birthday')
        doctor_obj.address = self.validated_data.get('address')
        doctor_obj.picture = self.validated_data.get('picture')
        doctor_obj.save()

    
        return user
    

class CustomRegisterSerializerNurse(RegisterSerializer):
    full_name = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=10, required=False)
    birthday = serializers.DateField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['phone_number'] = self.validated_data['full_name']
        data['full_name'] = self.validated_data['phone_number']
        data['birthday'] = self.validated_data['birthday']
        return data

    def save(self, request):
        #create a user and save it 
        user = super().save(request)
        user.full_name = self.validated_data['full_name']
        user.phone_number = self.validated_data['phone_number']
        user.save()
        
        # Create a nurse object and assign the user
        nurse_obj = nurse.objects.create(user=user)
        nurse_obj.birthday = self.validated_data.get('birthday')
        nurse_obj.save()


        return user
    

class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'full_name', 'speciality', 'address', 'picture']
