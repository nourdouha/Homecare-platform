#import the package used to solve the problem
from pyomo.environ import *
from datetime import date
from doctor.models import Doctor
from appointment.models import Appointment, Todayschedule
from .models import Ambulance, Driver
from .distance import calculate_distance

app_lat = [driver.doctor.MedicalCenter.latitude]
app_lon = [driver.doctor.MedicalCenter.longitude]
for appointment in today_appointments:
    app_lat.append(appointment.patient.address_latitude)  
    app_lon.append(appointment.patient.address_longitude)

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
nodes_count = patient_count+1


model.nodes = Set(initialize=range(patient_count+1))
model.Ambulances = Set(initialize=range(ambulance_count))
# create the decision variables     
model.x = Var(
    model.nodes, model.nodes, model.Ambulances,
    within=Binary,
    doc="1 if taken route from i-th to j-th place taken by k-th Ambulance, 0 otherwise"
             )

#calculate distance matrix
distance_matrix = [[0] * (patient_count + 1) for _ in range(patient_count + 1)]
for i in range(nodes_count):
    for j in range(i + 1, nodes_count):
        distance = calculate_distance(app_lat[i], app_lon[i], app_lat[j], app_lon[j])
        distance_matrix[i+1, j+1] = distance
        distance_matrix[j+1, i+1] = distance

#objective function 
model.obj_total_cost = Objective(
            sense=minimize,
            expr=(sum(
                 distance[i, j] * model.x[i, j, k]
                for i in range(nodes_count)
                for j in range(nodes_count) if j != i
                for k in range(ambulance_count))
            ),
            doc="Minimize total cost of routes taken by Ambulances"
        )

 
# add the constraints
# one patient is served by one ambulance
model.c=ConstraintList()
for j in range( 1,patient_count):
    model.c.add(sum(model.x[i, j, k] if i != j else 0 
                              for i in range(patient_count) 
                              for k in range(ambulance_count)) == 1)

#  departure and arrivals of each ambulance from hospital
for k in range(ambulance_count):
    model.c.add(sum(model.x[0, j, k] for j in range(1,nodes_count)) == 1)
    model.c.add(sum(model.x[i, 0, k] for i in range(1,nodes_count)) == 1)

# the number of vehicles coming in and out of a customer’s location is the same
for k in range(ambulance_count):
    for j in range(nodes_count):
        model.c.add(sum(model.x[i, j, k] if i != j else 0 
            for i in range(nodes_count)) -  sum(model.x[j, i, k] 
                for i in range(nodes_count)) == 0)
        
#time constraint # respect nursing time #respect ambulance time service
model.time_constraint_new = ConstraintList()
total_work_time = 4 * 60  # Total work time in minutes
ambulance_speed = 1  # Kilometer per minute
appointment_time = 30 #each patient has 30 min
for k in range(ambulance_count):
    for j in range(nodes_count):
        model.c.add(
            sum(model.x[i, j, k] if i != j else 0 for i in range(nodes_count))
            - sum(model.x[j, i, k] for i in range(nodes_count))
            == 0
        )

# Solve the model
solver = SolverFactory('glpk') # GLPK (GNU Linear Programming Kit)
results = solver.solve(model)

# Print the solution
if results.solver.status == SolverStatus.ok and results.solver.termination_condition == TerminationCondition.optimal:
    print("Optimal solution found")
    for i in nodes_count:
        for j in nodes_count:
            for k in ambulance_count:
                if model.x[i, j, k].value == 1:
                    print(f"Ambulance goes from node {i} to node {j}")
                
else:
    #we will use today_appointment without change 
    print("Solver did not find an optimal solution")




