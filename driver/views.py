from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import AppointmentSolutionSerializer
from .VRP import appointment_solution

class AppointmentSolutionView(APIView):
    def get(self, request):
        # Your VRP solution code here
        # ...

        # Create the serializer instance with the appointment_solution list
        serializer = AppointmentSolutionSerializer({'appointments': appointment_solution})

        return Response(serializer.data)

