import gurobipy as gp
from gurobipy import GRB

# Data
products = ['Product_A', 'Product_B', 'Product_C', 'Product_D']
predicted_demand = {'Product_A': 14, 'Product_B': 17, 'Product_C': 16, 'Product_D': 18}
available_supply = {'Product_A': 16, 'Product_B': 20, 'Product_C': 10, 'Product_D': 11}
demand_supply_gap = {'Product_A': 2, 'Product_B': 3, 'Product_C': 6, 'Product_D': 7}

# Creating a new model
model = gp.Model("Demand-Supply Matching")

# Variables
allocated_supply = model.addVars(products, name="Allocated_Supply")

# Objective: Minimize the total demand-supply gap
model.setObjective(gp.quicksum(demand_supply_gap[p] * (predicted_demand[p] - allocated_supply[p]) for p in products), GRB.MINIMIZE)

# Constraints
# 1. The available supply for each product cannot be exceeded
for p in products:
    model.addConstr(allocated_supply[p] <= available_supply[p], name=f"Supply_Limit_{p}")

# 2. The demand for each product must be met as closely as possible
for p in products:
    model.addConstr(allocated_supply[p] >= predicted_demand[p] - demand_supply_gap[p], name=f"Demand_Min_{p}")
    model.addConstr(allocated_supply[p] <= predicted_demand[p] + demand_supply_gap[p], name=f"Demand_Max_{p}")

# 3. The total supply allocated should not be more than the total available supply
model.addConstr(gp.quicksum(allocated_supply[p] for p in products) <= sum(available_supply.values()), name="Total_Supply_Limit")

# Optimize the model
model.optimize()

# Print the results
if model.status == GRB.OPTIMAL:
    for p in products:
        print(f"{p}: Allocated Supply = {allocated_supply[p].x}")
    print(f"Total Demand-Supply Gap: {model.objVal}")
else:
    print("No optimal solution found.")