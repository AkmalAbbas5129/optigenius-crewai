import pandas as pd
import numpy as np
from faker import Faker

# Initialize the Faker library
fake = Faker()


def generate_demand_supply_matching_predictions(num_stores=3, num_plants=3, seed=42):
    np.random.seed(seed)

    # Generate random store names using Faker and add "Store_" prefix
    store_names = [f"Store_{fake.city()}" for _ in range(num_stores)]

    # Generate random plant names with "Plant_" prefix
    plant_names = [f"Plant_{fake.city()}" for _ in range(num_plants)]

    # Generate random demand for stores (in units)
    store_demand = np.random.randint(100, 500, size=num_stores)

    # Generate random supply from plants (in units)
    plant_supply = np.random.randint(200, 600, size=num_plants)

    # Generate random distribution costs (in USD) from each plant to each store
    distribution_costs = np.random.randint(5, 20, size=(num_stores, num_plants))

    # Problem Statement, Objective, and Constraints
    problem_statement = (
        "A company needs to match the product supply from manufacturing plants to the demand from retail stores while minimizing distribution costs. "
        "Each store has a specific demand (in units), and each plant has a limited supply capacity (in units). "
        "The cost of distributing products (in USD) from plants to stores varies based on transportation, distance, and handling."
    )

    objective = "Minimize the total distribution cost (in USD) while fulfilling all store demands (in units) and respecting the plant supply capacity."

    constraints = """1. No plant can exceed its production capacity (in units).\n2. Each store's demand (in units) must be fully satisfied.
    """

    # Create individual DataFrames
    demand_df = pd.DataFrame({
        'Store Name': store_names,
        'Demand (Units)': store_demand
    })

    supply_df = pd.DataFrame({
        'Plant Name': plant_names,
        'Supply (Units)': plant_supply
    })

    distribution_costs_df = pd.DataFrame(
        distribution_costs,
        columns=plant_names,
        index=store_names
    )
    distribution_costs_df.index.name = 'Store Name'
    distribution_costs_df.columns.name = 'Plant Name'
    distribution_costs_df = distribution_costs_df.add_suffix(" (Distribution Cost USD)")

    # Create a dictionary to hold all data
    data_in_format = {
        'Store Demand (Units)': demand_df,
        'Plant Supply (Units)': supply_df,
        'Distribution Costs (USD)': distribution_costs_df
    }

    return problem_statement, objective, constraints, data_in_format


# prob, obj, cons, data = generate_demand_supply_matching_predictions()
# print(data)
# for name, df in data.items():
#     print(name)

# import random
#
#
# def generate_demand_supply_matching_predictions():
#     products = ['Product_A', 'Product_B', 'Product_C', 'Product_D']
#     predictions = {}
#
#     for product in products:
#         # Generate predicted demand and available supply
#         predicted_demand = random.randint(10, 20)
#         available_supply = random.randint(10, 20)
#
#         # Ensure supply is enough to handle the demand but add a realistic gap
#         if available_supply >= predicted_demand:
#             demand_supply_gap = available_supply - predicted_demand
#         else:
#             demand_supply_gap = predicted_demand - available_supply
#
#         predictions[product] = {
#             'Predicted_Demand_In_Units': predicted_demand,
#             'Available_Supply_In_Units': available_supply,
#             'Demand_Supply_Gap_In_Units': demand_supply_gap
#         }
#
#     return predictions
#
#
# if __name__ == "__main__":
#     print(generate_demand_supply_matching_predictions())
