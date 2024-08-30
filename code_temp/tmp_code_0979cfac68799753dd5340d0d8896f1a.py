import gurobipy as gp
from gurobipy import GRB

# Create a new model
model = gp.Model("Customer_Order_Fulfillment")

# Define data
order_quantity = [19, 12]
max_order_capacity = [70, 55]
available_inventory = [106, 101]
min_time = 4
max_time = 8

# Decision variables
order_time = model.addVar(vtype=GRB.INTEGER, name="order_time")

# Constraints
model.addConstr(order_time >= min_time, "MinTime")
model.addConstr(order_time <= max_time, "MaxTime")
model.addConstr(order_quantity[0] <= max_order_capacity[0], "MaxCapacity1")
model.addConstr(order_quantity[1] <= max_order_capacity[1], "MaxCapacity2")
model.addConstr(order_quantity[0] <= available_inventory[0], "Inventory1")
model.addConstr(order_quantity[1] <= available_inventory[1], "Inventory2")

# Objective: Minimize the order fulfillment time
model.setObjective(order_time, GRB.MINIMIZE)

# Optimize the model
model.optimize()

# Output the results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Order Fulfillment Time: {order_time.x} days")
else:
    print("No optimal solution found.")