import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()


def generate_transportation_optimization_predictions(num_customers=5, num_warehouses=3, seed=42):
    np.random.seed(seed)

    # Generate random customer names and warehouse names
    customer_names = [f"Customer_{fake.first_name()}" for _ in range(num_customers)]
    warehouse_names = [f"Warehouse_{j + 1}" for j in range(num_warehouses)]

    # Generate random shipping costs and capacities
    shipping_costs = np.random.uniform(1, 10, size=(num_customers, num_warehouses))
    capacities = np.random.randint(200, 1000, size=num_warehouses)

    # Generate random demand for each customer
    customer_demand = np.random.randint(100, 500, size=num_customers)

    # Problem Statement, Objective, and Constraints
    problem_statement = (
        "Optimize the transportation of goods from warehouses to customers to minimize transportation costs while ensuring timely delivery."
    )

    objective = "Minimize the total transportation cost while meeting delivery deadlines and customer demands."

    constraints ="""1. Each route has a cost and capacity limit.\n2. Delivery deadlines must be met.\n3. The total amount shipped must meet customer demand."""

    # Create DataFrames
    shipping_costs_df = pd.DataFrame(shipping_costs, columns=warehouse_names, index=customer_names)
    capacities_df = pd.DataFrame(capacities, index=warehouse_names, columns=['Capacity'])
    customer_demand_df = pd.DataFrame(customer_demand, index=customer_names, columns=['Demand'])

    # Create a dictionary to hold all data
    data_in_format = {
        'Shipping Costs': shipping_costs_df,
        'Warehouse Capacities': capacities_df,
        'Customer Demand': customer_demand_df
    }

    return problem_statement, objective, constraints, data_in_format
