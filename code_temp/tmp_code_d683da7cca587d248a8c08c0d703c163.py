import gurobipy as gp
from gurobipy import GRB

# Define the model
model = gp.Model("CustomerOrderFulfillment")

# Parameters
order_quantity = 19
min_fulfillment_time = 3
max_fulfillment_time = 7
min_capacity = 54
max_capacity = 58
min_inventory = 101
max_inventory = 108

# Decision Variables
fulfillment_time = model.addVar(vtype=GRB.INTEGER, name="fulfillment_time")
shipment_capacity = model.addVar(vtype=GRB.INTEGER, name="shipment_capacity")
inventory_level = model.addVar(vtype=GRB.INTEGER, name="inventory_level")

# Constraints
model.addConstr(fulfillment_time >= min_fulfillment_time, "MinFulfillmentTime")
model.addConstr(fulfillment_time <= max_fulfillment_time, "MaxFulfillmentTime")
model.addConstr(shipment_capacity >= min_capacity, "MinCapacity")
model.addConstr(shipment_capacity <= max_capacity, "MaxCapacity")
model.addConstr(inventory_level >= min_inventory, "MinInventory")
model.addConstr(inventory_level <= max_inventory, "MaxInventory")
model.addConstr(inventory_level - order_quantity >= 0, "InventoryAfterOrder")

# Objective: Minimize inventory shortages and avoid exceeding the maximum order capacity
model.setObjective(inventory_level - order_quantity, GRB.MINIMIZE)

# Optimize the model
model.optimize()

# Output the results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Fulfillment Time: {fulfillment_time.x} days")
    print(f"Optimal Shipment Capacity: {shipment_capacity.x} units")
    print(f"Optimal Inventory Level: {inventory_level.x} units")
else:
    print("No optimal solution found.")