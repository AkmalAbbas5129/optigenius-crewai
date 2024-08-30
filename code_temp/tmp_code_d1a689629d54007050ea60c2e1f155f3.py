from gurobipy import Model, GRB

# Data
products = ['A', 'B', 'C', 'D']
demand = {'A': 12, 'B': 17, 'C': 15, 'D': 18}
supply = {'A': 17, 'B': 14, 'C': 11, 'D': 19}
gap = {'A': 5, 'B': 3, 'C': 4, 'D': 1}

# Create a new model
model = Model("demand_supply_matching")

# Create variables
allocation = model.addVars(products, name="allocation", vtype=GRB.CONTINUOUS)

# Set objective: Minimize the total demand-supply gap
model.setObjective(sum((demand[p] - allocation[p]) * gap[p] for p in products), GRB.MINIMIZE)

# Add constraints: The supply allocated to each product must not exceed its available supply
model.addConstrs((allocation[p] <= supply[p] for p in products), name="supply_capacity")

# Optimize model
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    for p in products:
        print(f"Product {p}: Allocation = {allocation[p].X}, Demand = {demand[p]}, Supply = {supply[p]}, Gap = {demand[p] - allocation[p].X}")
else:
    print("No optimal solution found.")