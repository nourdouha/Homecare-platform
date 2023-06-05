import numpy as np
from pyomo.environ import *
from appointment.models import Todayschedule
from .models import Driver
from .distance import calculate_distance
#create model and resolve by pyomo package

driver = Driver.objects.get(id)
today_appointments = Todayschedule.get_appointments(driver.doctor)
patient_count = min(len(today_appointments), 5)
for Ambulance_count in range(1,max_Ambulance_count):

    model = ConcreteModel()
# create index from patients and ambulances
    model.patient = Set(initialize=range(patient_count))
    model.Ambulances = Set(initialize=range(Ambulance_count))
    
# create the decision variables  a 3D binary variable     
    model.x = Var(
             model.patient, model.patient, model.Ambulances,
             within=Binary,
            doc="1 if taken route from i-th to j-th place taken by k-th Ambulance, 0 otherwise"
             )
    
# add objective function

    model.obj_total_cost = Objective(
            sense=minimize,
            expr=(sum(
                 distance[i, j] * model.x[i, j, k]
                for i in range(patient_count)
                for j in range(patient_count) if j != i
                for k in range(Ambulance_count))+
                  sum(TH[j] * model.x[i, j, k] if i != j else 0 
                         for i in range(patient_count) for j in range (1,patient_count) for k in range(Ambulance_count))
            ),
            doc="Minimize total cost of routes taken by Ambulances"
        )

# add the constraints
    # one patient is served by one ambulance
    model.c=ConstraintList()
    for j in range( 1,patient_count):
        model.c.add(sum(model.x[i, j, k] if i != j else 0 
                              for i in range(patient_count) 
                              for k in range(Ambulance_count)) == 1)

    #  departure and arrivals of each ambulance from hospital
    for k in range(Ambulance_count):
        model.c.add(sum(model.x[0, j, k] for j in range(1,patient_count)) == 1)
        model.c.add(sum(model.x[i, 0, k] for i in range(1,patient_count)) == 1)

    # the number of vehicles coming in and out of a customer’s location is the same
    for k in range(Ambulance_count):
        for j in range(patient_count):
             model.c.add(sum(model.x[i, j, k] if i != j else 0 
                                  for i in range(patient_count)) -  sum(model.x[j, i, k] 
                                                                         for i in range(patient_count)) == 0)

    # respect nursing time
    for k in range(Ambulance_count):
         model.c.add(sum(TH[j] * model.x[i, j, k] if i != j else 0 
                         for i in range(patient_count) for j in range (1,patient_count)) <= nursing_time) 
    
    #respect ambulance time service
    for k in range(Ambulance_count):
         model.c.add((sum(TH[j] * model.x[i, j, k] if i != j else 0 
                         for i in range(patient_count) for j in range (1,patient_count))+
                      sum(distance[i, j] * model.x[i, j, k] for i in range(patient_count)
                         for j in range(patient_count) if j != i)) <= Ambulance_time)
   
    #Ambulance serves >n patients
#     for k in range(Ambulance_count):            
#         model.c.add(  sum(model.x[i, j, k] if i != j else 0 
#                 for i in range(patient_count)
#                 for j in range(patient_count) ) >=3)
        
# subtours elimination constraint
    subtours = []
    for i in range(2,patient_count):
         subtours += itertools.combinations(range(1,patient_count), i)

    for s in subtours:
         model.c.add(sum(model.x[i, j, k] if i !=j else 0 for i, j in itertools.permutations(s,2) 
                         for k in range(Ambulance_count)) <= len(s) - 1)
    
    solver = SolverFactory('glpk')
    result = solver.solve(model,tee=False)
    if  (result.solver.status == SolverStatus.ok) and (result.solver.termination_condition == TerminationCondition.optimal):
            break