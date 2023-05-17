from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from .models import User

from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer

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

