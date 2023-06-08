from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from .models import User, Patient, Medical_file
from rest_framework import viewsets
from dj_rest_auth.registration.views import RegisterView
from .serializers import  CustomRegisterSerializerPatient, MedicalFileSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

 #patient view (new user , new patient)

class CustomRegisterViewPatient(RegisterView):
    serializer_class = CustomRegisterSerializerPatient
    queryset = User.objects.all()

    def create_user(self, serializer):
        user = serializer.save(self.request)


        # Create a patient object
        patient = patient.objects.create(user=user)
        patient.birthday = serializer.validated_data.get('birthday')
        patient.address = serializer.validated_data.get('address')
        patient.save()

        return user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            #user = serializer.save(request)
            patient_obj = serializer.save(request)
            data = {
                "username": patient_obj.user.username,
                "email": patient_obj.user.email,
                "phone_number": patient_obj.user.phone_number,
                "full_name": patient_obj.user.full_name,
                "address_latitude": patient_obj.address_latitude,
                "address_longitude": patient_obj.address_longitude,
                "birthday": patient_obj.birthday,
                "address": patient_obj.user.address,
                "picture": patient_obj.picture,
            }
            return JsonResponse(data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class MedicalFileAPIView(APIView):
    def post(self, request):
        serializer = MedicalFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



