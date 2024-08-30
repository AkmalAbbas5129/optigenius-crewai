from gurobipy import Model, GRB, quicksum

# Data
fulfillment_times = [9, 3]
order_quantities = [6, 8]
max_order_capacity = [69, 66]
inventory = [102, 105]

# Create a new model
model = Model("CustomerOrderFulfillment")

# Decision variables: order quantities for each order
order_vars = model.addVars(len(order_quantities), vtype=GRB.INTEGER, name="order")

# Set objective: minimize the total fulfillment time weighted by order quantities
model.setObjective(quicksum(fulfillment_times[i] * order_vars[i] for i in range(len(order_quantities))), GRB.MINIMIZE)

# Constraints
for i in range(len(order_quantities)):
    model.addConstr(order_vars[i] <= inventory[i], f"Inventory_{i}")  # Inventory constraint
    model.addConstr(order_vars[i] <= max_order_capacity[i], f"Capacity_{i}")  # Capacity constraint

# Optimize model
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    for v in model.getVars():
        print(f'{v.varName}: {v.x}')
    print(f'Optimal objective value: {model.objVal}')
else:
    print('No optimal solution found.')