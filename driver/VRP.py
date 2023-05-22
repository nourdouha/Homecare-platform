import numpy as np
from pyomo.environ import *
from appointment.models import Todayschedule
from .models import Driver
from .distance import calculate_distance



# Get today's appointments for each driver
driver = Driver.objects.get(id)
today_appointments = Todayschedule.get_appointments(driver.doctor)

# Get the coordinates for medical center + patients to calculate distances
app_lat = [driver.doctor.MedicalCenter.latitude]
app_lon = [driver.doctor.MedicalCenter.longitude]
for appointment in today_appointments:
    app_lat.append(appointment.patient.address_latitude)  
    app_lon.append(appointment.patient.address_longitude)


# Set data
num_customers = min(len(today_appointments), 5)
num_vehicles = 1
depot = 0
customers = range(1, num_customers + 1)
nodes = np.arange(num_customers + 1)

# Calculate distance matrix
distance_matrix = np.zeros((num_customers + 1, num_customers + 1))
for i in range(num_customers):
    for j in range(i + 1, num_customers):
        distance = calculate_distance(app_lat[i], app_lon[i], app_lat[j], app_lon[j])
        distance_matrix[i+1, j+1] = distance
        distance_matrix[j+1, i+1] = distance

    



# Create the model
model = ConcreteModel()

# Decision variables
model.x = Var(nodes, nodes, within=Binary)

# Objective function (minimize total distance)
model.obj = Objective(expr=sum(distance_matrix[i, j] * model.x[i, j] for i in nodes for j in nodes))

# Constraints


# enforcing start point and end point

model.start_end = ConstraintList()
model.start_end.add(
    sum(model.x[depot, node] for node in nodes if node != depot) == 1
)
model.start_end.add(
    sum(model.x[node, depot] for node in nodes if node != depot) == 1
)

# Routing Connectivity Constraint 
model.connectivity = Constraint(
    expr=sum(model.x[depot, j] for j in customers) == sum(model.x[i, depot] for i in customers)
)


# all patients must be visited  one time
model.visitation = ConstraintList()

for node in nodes:
    if node != depot:
        model.visitation.add(
            sum(model.x[i, node] for i in nodes if i != node) == 1
        )

# Time constraints 
model.time_constraint = ConstraintList()
total_work_time = 4 * 60  # Total work time in minutes
ambulance_speed = 1  # Kilometer per minute
appointment_time = 30 #each patient has 30 min

for node in nodes:
    if node != depot:
        model.time_constraint.add(
            sum(model.x[i, node] * distance_matrix[i, node] * ambulance_speed for i in nodes if i != node)
            <= total_work_time - appointment_time
        )


# Solve the model
solver = SolverFactory('glpk') # GLPK (GNU Linear Programming Kit)
results = solver.solve(model)

# Print the solution
if results.solver.status == SolverStatus.ok and results.solver.termination_condition == TerminationCondition.optimal:
    print("Optimal solution found")
    for i in nodes:
        for j in nodes:
            if model.x[i, j].value == 1:
                print(f"Ambulance goes from node {i} to node {j}")
                
else:
    #we will use today_appointment without change 
    print("Solver did not find an optimal solution")
