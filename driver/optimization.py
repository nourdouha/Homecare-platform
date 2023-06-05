#import the package used to solve the problem
from pyomo.environ import *
from datetime import date
from doctor.models import Doctor
from appointment.models import Appointment, Todayschedule
from .models import Ambulance, Driver
from .distance import calculate_distance

#get the appointments from all doctors 
doctors = Doctor.objects.all()
today = date.today()

appointments = []
for doctor in doctors:
    doctor_appointments = Todayschedule.get_appointments(doctor_id=doctor.id)
    appointments.extend(doctor_appointments)
#calculate the distance using addresses associated with appointment's patients 

model = ConcreteModel()
# create index from patients and ambulances
ambulance_count = len(Ambulance.objects.all())
patient_count = len(appointments)

model.patient = Set(initialize=range(patient_count))
model.Ambulances = Set(initialize=range(ambulance_count))
# create the decision variables     
model.x = Var(
    model.patient, model.patient, model.Ambulances,
    within=Binary,
    doc="1 if taken route from i-th to j-th place taken by k-th Ambulance, 0 otherwise"
             )

#calculate distance matrix
distance_matrix = [[0] * (patient_count + 1) for _ in range(patient_count + 1)]
for i in range(patient_count):
    for j in range(i + 1, patient_count):
        distance = calculate_distance(app_lat[i], app_lon[i], app_lat[j], app_lon[j])
        distance_matrix[i+1, j+1] = distance
        distance_matrix[j+1, i+1] = distance

#objective function 



#decision variables


#contraints 


