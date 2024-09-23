import pandas as pd
import numpy as np
from faker import Faker

# Initialize the Faker library
fake = Faker()


def generate_customer_order_fulfillment_predictions(num_customers=2, num_warehouses=3, seed=42):
    np.random.seed(seed)

    # Generate random customer names using Faker and add "Customer_" prefix
    customer_names = [f"Customer_{fake.first_name()}" for _ in range(num_customers)]

    # Generate random customer demands (in units)
    customer_demand = np.random.randint(50, 150, size=num_customers)

    # Generate random warehouse supplies (in units)
    warehouse_ids = [f"Warehouse_{fake.city()}" for j in range(num_warehouses)]
    warehouse_supply = np.random.randint(100, 300, size=num_warehouses)

    # Generate random shipping costs (in USD) from each warehouse to each customer
    shipping_costs = np.random.randint(1, 10, size=(num_customers, num_warehouses))

    # Problem Statement, Objective, and Constraints
    problem_statement = (
        "A company needs to fulfill customer orders from multiple warehouses while minimizing shipping costs. "
        "Each customer has a specific demand (in units), and each warehouse has a limited supply of products (in units). "
        "The cost of shipping products (in USD) from warehouses to customers varies based on distance and logistics."
    )

    objective = "Minimize the total shipping cost (in USD) while fulfilling all customer orders (in units)."

    constraints ="""1. Each customer's demand (in units) must be fully satisfied.\n2. Each warehouse can only ship products up to its available supply (in units).\n3. Shipping costs vary between different warehouse-customer pairs (in USD)."""

    # Create individual DataFrames
    demand_df = pd.DataFrame({
        'Customer Name': customer_names,
        'Demand (Units)': customer_demand
    })

    supply_df = pd.DataFrame({
        'Warehouse': warehouse_ids,
        'Supply (Units)': warehouse_supply
    })

    shipping_costs_df = pd.DataFrame(
        shipping_costs,
        columns=warehouse_ids,
        index=customer_names
    )
    shipping_costs_df.index.name = 'Customer Name'
    shipping_costs_df.columns.name = 'Warehouse'
    shipping_costs_df = shipping_costs_df.add_suffix(" (Shipping Cost USD)")

    # Create a dictionary to hold all data
    data_in_format = {
        'Customer Demand (Units)': demand_df,
        'Warehouse Supply (Units)': supply_df,
        'Shipping Costs (USD)': shipping_costs_df
    }

    return problem_statement, objective, constraints, data_in_format

##########################################################################
# import pandas as pd
# import numpy as np
#
# # Parameters for generating data
# num_products = 5  # Number of products
# np.random.seed(42)
#
#
# def generate_problem_statement(df):
#     problem_statement = """
#     The company is facing challenges in optimizing its customer order fulfillment process across various products.
#     Current fulfillment times vary significantly, ranging from {} to {} days, which leads to potential delays in meeting customer demand.
#     The company seeks to optimize the fulfillment process to minimize delays while considering inventory availability and operational capacity.
#     """.format(df['Order Fulfillment Time (in days)'].min(), df['Order Fulfillment Time (in days)'].max())
#     return problem_statement
#
#
# def generate_objective(df):
#     objective = """
#     The objective is to minimize the order fulfillment time for all products while ensuring that the available inventory is used efficiently.
#     The company aims to fulfill customer orders promptly without exceeding the maximum capacity of each product and avoiding stockouts.
#     """
#     return objective
#
#
# def generate_constraints(df):
#     constraints = """
#     Constraints:
#     1. The order quantity for each product must not exceed the maximum fulfillment capacity, which ranges from {} to {} units across different products.
#     2. The total fulfilled quantity must not exceed the available inventory, which varies from {} to {} units across products.
#     3. The company should aim to reduce the fulfillment time, currently ranging from {} to {} days, without overloading the operational capacity.
#     """.format(df['Max Order Capacity'].min(), df['Max Order Capacity'].max(),
#                df['Available Inventory'].min(), df['Available Inventory'].max(),
#                df['Order Fulfillment Time (in days)'].min(), df['Order Fulfillment Time (in days)'].max())
#     return constraints
#
#
# def generate_customer_order_fulfillment_predictions():
#     # Generate random data
#     data = {
#         "Product ID": np.arange(1, num_products + 1),
#         "Order Fulfillment Time (in days)": np.random.randint(5, 15, size=num_products),  # Random days between 5 and 15
#         "Order Quantity": np.random.randint(10, 100, size=num_products),  # Random quantity between 10 and 100
#         "Max Order Capacity": np.random.randint(40, 80, size=num_products),  # Max capacity between 40 and 80
#         "Available Inventory": np.random.randint(50, 150, size=num_products)  # Available inventory between 50 and 150
#     }
#
#     # Create a DataFrame
#     df = pd.DataFrame(data)
#     # Generating problem statement, objective, and constraints
#     problem_statement = generate_problem_statement(df)
#     objective = generate_objective(df)
#     constraints = generate_constraints(df)
#
#     return problem_statement, objective, constraints, df


########################################################################
# import random
#
#
# def generate_random_values(num_products, value_range):
#     return [random.randint(value_range[0], value_range[1]) for _ in range(num_products)]
#
#
# def generate_customer_order_fulfillment_predictions():
#     num_products = 2  # Adjust number of products as needed
#     order_fulfillment_time_range = (2, 10)  # in days
#     order_quantity_range = (5, 20)  # in units
#     max_order_capacity_range = (50, 70)  # in units
#     available_inventory_range = (100, 110)  # in units
#
#     # Generate predictions for each product
#     order_fulfillment_time = generate_random_values(num_products, order_fulfillment_time_range)
#     order_quantity = generate_random_values(num_products, order_quantity_range)
#     max_order_capacity = generate_random_values(num_products, max_order_capacity_range)
#     available_inventory = generate_random_values(num_products, available_inventory_range)
#
#     scenario = "Customer Order Fulfillment Optimization"
#
#     # Segregating data by product
#     product_data = []
#     for i in range(num_products):
#         product_info = {
#             "product_id": i + 1,
#             "order_fulfillment_time_in_days": order_fulfillment_time[i],
#             "order_quantity": order_quantity[i],
#             "max_order_capacity": max_order_capacity[i],
#             "available_inventory": available_inventory[i]
#         }
#         product_data.append(product_info)
#
#     return product_data
#
#
# # Example usage
# # dummy_data = generate_customer_order_fulfillment_predictions()
# # for product in dummy_data:
# #     print(product)
