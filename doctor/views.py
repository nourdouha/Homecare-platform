from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from .models import Doctor,User,nurse
from dj_rest_auth.registration.views import RegisterView
from .serializers import  CustomRegisterSerializerDoctor , CustomRegisterSerializerNurse

#Doctor view    

class CustomRegisterViewDoctor(RegisterView):
    serializer_class = CustomRegisterSerializerDoctor
    queryset = User.objects.all()

    def create_user(self, serializer):
        user = serializer.save(self.request)

        # Create a doctor object
        doctor_obj = Doctor.objects.create(user=user)
        doctor_obj.speciality = serializer.validated_data.get('speciality')
        doctor_obj.birthday = serializer.validated_data.get('birthday')
        doctor_obj.address = serializer.validated_data.get('address')
        doctor_obj.save()

        return user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            doctor_obj = serializer.save(request)
            data = {
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "full_name": user.full_name,
                "speciality": doctor_obj.speciality,
                "birthday": doctor_obj.birthday,
                "address": doctor_obj.address,
                "picture": doctor_obj.picture,
            }
            return JsonResponse(data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

#nurse views
class CustomRegisterViewNurse(RegisterView):
    serializer_class = CustomRegisterSerializerNurse
    queryset = User.objects.all()

    def create_user(self, serializer):
        user = serializer.save(self.request)

        # Create a nurse object
        nurse_obj = nurse.objects.create(user=user)
        nurse_obj.birthday = serializer.validated_data.get('birthday')
        nurse_obj.save()

        return user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            #user = serializer.save(request)
            nurse_obj = serializer.save(request)
            data = {
                "username": nurse_obj.user.username,
                "email": nurse_obj.user.email,
                "phone_number": nurse_obj.user.phone_number,
                "full_name": nurse_obj.user.full_name,
                "birthday": nurse_obj.birthday,
            }
            return JsonResponse(data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

#get doctors list 

def get_doctors(request):
    doctors = Doctor.objects.all()
    data = []
    for doctor in doctors:
        data.append({
            'full_name': doctor.user.full_name,
            'speciality': doctor.speciality,
            'address': doctor.address,
            'picture' : doctor.picture
            # Add other fields you want to include
        })
    return JsonResponse(data, safe=False)

from .serializers import DoctorSerializer

def get_doctorss(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return JsonResponse(serializer.data, safe=False)
