import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()


def generate_inventory_optimization_predictions(num_products=5, num_warehouses=3, seed=42):
    np.random.seed(seed)

    # Generate random product names and warehouse names
    product_names = [f"Product_{fake.word()}" for _ in range(num_products)]
    warehouse_names = [f"Warehouse_{j + 1}" for j in range(num_warehouses)]

    # Generate random holding costs and capacities
    holding_costs = np.random.uniform(1, 10, size=num_products)
    capacities = np.random.randint(500, 2000, size=num_warehouses)

    # Generate random demand forecast for each product at each warehouse
    demand_forecast = np.random.randint(50, 200, size=(num_products, num_warehouses))

    # Problem Statement, Objective, and Constraints
    problem_statement = (
        "Optimize inventory levels across multiple warehouses to minimize holding costs while meeting customer demand. "
        "The company faces trade-offs between holding too much inventory (high holding costs) and too little (stockouts)."
    )

    objective = "Minimize the total holding costs while maintaining sufficient inventory levels to meet customer demand."

    constraints = [
        "1. Inventory levels should meet the forecasted demand.",
        "2. Each warehouse has a maximum storage capacity.",
        "3. Holding costs must be minimized."
    ]

    # Create DataFrames
    holding_costs_df = pd.DataFrame(holding_costs, index=product_names, columns=['Holding Cost per Unit'])
    capacities_df = pd.DataFrame(capacities, index=warehouse_names, columns=['Capacity'])
    demand_forecast_df = pd.DataFrame(demand_forecast, columns=warehouse_names, index=product_names)

    # Create a dictionary to hold all data
    data_in_format = {
        'Holding Costs': holding_costs_df,
        'Warehouse Capacities': capacities_df,
        'Demand Forecast': demand_forecast_df
    }

    return problem_statement, objective, constraints, data_in_format
