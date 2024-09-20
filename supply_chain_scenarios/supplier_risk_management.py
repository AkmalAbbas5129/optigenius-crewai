import pandas as pd
import numpy as np
from faker import Faker

# Initialize the Faker library
fake = Faker()


def generate_supplier_risk_predictions(num_suppliers=5, demand=1000, risk_threshold=0.2, seed=42):
    np.random.seed(seed)

    # Generate random supplier names using Faker and add "Supplier_" prefix
    supplier_names = [f"Supplier_{fake.company()}" for _ in range(num_suppliers)]

    # Generate random supply capacity (in units) for each supplier
    supplier_capacity = np.random.randint(200, 500, size=num_suppliers)

    # Generate random procurement cost (in USD) per unit for each supplier
    procurement_costs = np.random.randint(50, 150, size=num_suppliers)

    # Generate random risk scores (between 0 and 1) for each supplier
    supplier_risk = np.random.rand(num_suppliers)

    # Problem Statement, Objective, and Constraints
    problem_statement = (
        "A company must select suppliers to meet its demand while minimizing both procurement costs and supply chain risk. "
        "Each supplier has a limited capacity (in units), a cost per unit (in USD), and an associated risk score (between 0 and 1). "
        "The goal is to meet the company's total demand by sourcing products from these suppliers while keeping the overall risk below a certain threshold."
    )

    objective = "Minimize the total procurement cost (in USD) while keeping the overall risk below the risk threshold and meeting the demand."

    constraints = f"""1. The total supply from selected suppliers must meet the company's demand of {demand} units.\n2. No supplier can exceed their capacity limit (in units).\n3. The overall supply risk must stay below the risk threshold of {risk_threshold}.\n4. The cost of procurement should be minimized."""

    # Create individual DataFrames
    capacity_df = pd.DataFrame({
        'Supplier Name': supplier_names,
        'Supply Capacity (Units)': supplier_capacity
    })

    cost_df = pd.DataFrame({
        'Supplier Name': supplier_names,
        'Procurement Cost (USD/Unit)': procurement_costs
    })

    risk_df = pd.DataFrame({
        'Supplier Name': supplier_names,
        'Risk Score (0-1)': supplier_risk
    })

    # Create a dictionary to hold all data
    data_in_format = {
        'Supplier Capacity (Units)': capacity_df,
        'Procurement Cost (USD/Unit)': cost_df,
        'Supplier Risk (Score)': risk_df
    }

    return problem_statement, objective, constraints, data_in_format

# import random
#
#
# def generate_supplier_risk_predictions():
#     # List of suppliers
#     suppliers = ['Supplier A', 'Supplier B', 'Supplier C']
#
#     # Dictionary to store predictions for each supplier
#     predictions = {}
#
#     for supplier in suppliers:
#         # Risk Score: Simulates the risk associated with the supplier.
#         # Lower values indicate lower risk and higher values indicate higher risk.
#         risk_score = random.uniform(0.2, 0.8)  # Realistic risk scores between 0.2 and 0.8
#
#         # Predicted Delays: Simulates potential delays in days.
#         # This reflects how often suppliers may delay their deliveries.
#         predicted_delays = random.randint(1, 7)  # Realistic delays between 1 and 7 days
#
#         # Cost Variability: Represents how much the supplier's costs might fluctuate.
#         # A lower percentage indicates less fluctuation.
#         cost_variability = random.uniform(0.05, 0.15)  # Realistic cost variability between 5% and 15%
#
#         # Store the generated values in the predictions dictionary
#         predictions[supplier] = {
#             'Risk Score': risk_score,
#             'Predicted_Delays_In_Days': predicted_delays,
#             'Cost_Variability_In_Percentage': cost_variability
#         }
#
#     # Return the dictionary containing predictions for all suppliers
#     return predictions
#
#
# if __name__ == "__main__":
#     print(generate_supplier_risk_predictions())
