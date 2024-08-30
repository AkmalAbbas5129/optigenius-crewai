from gurobipy import Model, GRB, quicksum

# Data for the products
products = ['Product_A', 'Product_B', 'Product_C', 'Product_D']

historical_demand = {
    'Product_A': [82, 170, 194, 151, 104, 185, 123, 138, 132, 148, 230, 182],
    'Product_B': [133, 112, 175, 152, 114, 193, 240, 203, 204, 190, 162, 158],
    'Product_C': [100, 125, 136, 131, 160, 115, 133, 222, 157, 172, 176, 175],
    'Product_D': [114, 155, 83, 183, 202, 127, 240, 172, 133, 178, 200, 182]
}

predicted_demand = {
    'Product_A': 257,
    'Product_B': 283,
    'Product_C': 156,
    'Product_D': 235
}

confidence_intervals = {
    'Product_A': (238, 274),
    'Product_B': (273, 299),
    'Product_C': (137, 172),
    'Product_D': (222, 255)
}

trend_factors = {
    'Product_A': 1.0595334745710965,
    'Product_B': 1.0766510932199334,
    'Product_C': 0.9179694835392407,
    'Product_D': 1.0273849269297812
}

seasonality_factors = {
    'Product_A': 1.0999908476216573,
    'Product_B': 0.9963187524232111,
    'Product_C': 1.097376223722942,
    'Product_D': 0.9209119924511983
}

promotion_effects = {
    'Product_A': 1.2492523560968258,
    'Product_B': 1.1070910943917105,
    'Product_C': 1.1031060872840805,
    'Product_D': 1.015704262119156
}

economic_factors = {
    'Product_A': 0.9600320871180341,
    'Product_B': 0.9738296161301375,
    'Product_C': 0.9738708584709184,
    'Product_D': 1.0329583651294165
}

competitor_actions = {
    'Product_A': 0.9587749691711952,
    'Product_B': 1.0795295832257914,
    'Product_C': 0.9290263724439698,
    'Product_D': 0.9641963928157361
}

# Initialize the Gurobi model
model = Model("DemandForecasting")

# Variables: Adjusted demand for each product
adjusted_demand = model.addVars(products, lb=0, name="AdjustedDemand")

# Objective: Minimize the discrepancy between adjusted and predicted demand
model.setObjective(
    quicksum((adjusted_demand[p] - predicted_demand[p]) * (adjusted_demand[p] - predicted_demand[p]) for p in products),
    GRB.MINIMIZE
)

# Constraints: Adjusted demand should fall within the confidence intervals
for p in products:
    model.addConstr(adjusted_demand[p] >= confidence_intervals[p][0], f"LowerBound_{p}")
    model.addConstr(adjusted_demand[p] <= confidence_intervals[p][1], f"UpperBound_{p}")

# Constraints: Adjusted demand considering influencing factors
influencing_factors = {
    p: trend_factors[p] * seasonality_factors[p] * promotion_effects[p] * economic_factors[p] * competitor_actions[p]
    for p in products
}

for p in products:
    model.addConstr(adjusted_demand[p] == predicted_demand[p] * influencing_factors[p], f"Influence_{p}")

# Optimize the model
model.optimize()

# Output the results
for p in products:
    print(f"{p}: Adjusted Demand = {adjusted_demand[p].X}")