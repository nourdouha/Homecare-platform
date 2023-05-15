from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from .models import User,doctor,nurse,patient,driver

from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer, CustomRegisterSerializerDoctor

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    queryset = User.objects.all()

def aPage(request):
    serializer = CustomRegisterSerializer(data=request.data)
    if request.method == 'POST':
        if serializer.is_valid():
            # Create new user object with form data
            user = serializer.save(request)
        
        # Return JSON response with user data
            data = {
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "full_name": user.full_name,
            }
            return JsonResponse(data, status=201)
        else:
            return JsonResponse(data, status=201)
    else:
        # Handle GET request for the page
        user = User.objects.get(pk=1)
        data = {
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "full_name": user.full_name,
        }
        return JsonResponse(data)
     
    #when I passed the data directly to the JSON dataformat I got an error


    #Doctor view
    
from django.contrib.auth.models import Group

class CustomRegisterViewDoctor(RegisterView):
    serializer_class = CustomRegisterSerializerDoctor
    queryset = User.objects.all()

    def create_user(self, serializer):
        user = serializer.save(self.request)

        # Add the user to the "doctor" group
        doctor_group = Group.objects.get(name='doctor')
        doctor_group.user_set.add(user)

        # Create a doctor object
        doctor = doctor.objects.create(user=user)
        doctor.speciality = serializer.validated_data.get('speciality')
        doctor.birthday = serializer.validated_data.get('birthday')
        doctor.address = serializer.validated_data.get('address')
        doctor.save()

        return user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            data = {
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "full_name": user.full_name,
                "speciality": user.doctor_obj.speciality,
                "birthday": user.doctor_obj.birthday,
                "address": user.doctor_obj.address,
            }
            return JsonResponse(data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

