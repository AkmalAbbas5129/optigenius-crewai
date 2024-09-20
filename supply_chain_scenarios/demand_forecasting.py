import pandas as pd
import numpy as np
from faker import Faker

# Initialize the Faker library
fake = Faker()


def generate_demand_forecasting_predictions(num_products=5, num_months=12, seed=42):
    np.random.seed(seed)

    # Generate random product names using Faker and add "Product_" prefix
    product_names = [f"Product_{fake.word()}" for _ in range(num_products)]

    # Generate historical sales data (in units) for each product over the past year
    historical_sales = np.random.randint(1000, 5000, size=(num_products, 12))

    # Generate random forecasted demand (in units) for the next 12 months
    forecasted_demand = historical_sales.mean(axis=1) + np.random.randint(-500, 500, size=num_products)

    # Generate seasonal factors (e.g., seasonal peaks or troughs)
    seasonal_factors = np.sin(np.linspace(0, 2 * np.pi, num_months)) + np.random.normal(0, 0.1, size=num_months)

    # Adjust forecasted demand based on seasonal factors
    forecasted_demand_matrix = np.outer(forecasted_demand, seasonal_factors) + np.random.randint(-200, 200, size=(
    num_products, num_months))

    # Problem Statement, Objective, and Constraints
    problem_statement = (
        "The company needs to forecast the monthly demand for its products over the next 12 months. "
        "The forecasting model should use historical sales data and account for seasonal variations to predict future demand accurately."
    )

    objective = "Accurately forecast the monthly demand for each product to optimize inventory levels and improve supply chain efficiency."

    constraints = [
        "1. The forecast should be based on historical sales data and seasonal patterns.",
        "2. The forecasting model should achieve a reasonable level of accuracy.",
        "3. Seasonal factors and potential anomalies should be considered in the forecast."
    ]

    # Create DataFrames for historical sales, forecasted demand, and seasonal factors
    historical_sales_df = pd.DataFrame(
        historical_sales,
        columns=[f"Month_{i + 1}" for i in range(12)],
        index=product_names
    )

    forecasted_demand_df = pd.DataFrame(
        forecasted_demand_matrix,
        columns=[f"Month_{i + 1}" for i in range(num_months)],
        index=product_names
    )

    seasonal_factors_df = pd.DataFrame(
        seasonal_factors.reshape(1, -1),
        columns=[f"Month_{i + 1}" for i in range(num_months)],
        index=['Seasonal Factors']
    )

    # Create a dictionary to hold all data
    data_in_format = {
        'Historical Sales (Units)': historical_sales_df,
        'Forecasted Demand (Units)': forecasted_demand_df,
        'Seasonal Factors': seasonal_factors_df
    }

    return problem_statement, objective, constraints, data_in_format

# import random
#
#
# def generate_demand_forecasting_predictions():
#     products = ['Product_A', 'Product_B', 'Product_C', 'Product_D']
#     predictions = {}
#
#     for product in products:
#         # Historical demand with a seasonal trend
#         historical_demand = [random.randint(80, 200) + 20 * ((i % 12) // 3) for i in range(12)]
#
#         # Predicted demand with a base value, trend, and seasonality
#         base_demand = random.randint(100, 250)
#         trend = random.uniform(0.9, 1.1)  # Long-term trend factor
#         seasonality = random.uniform(0.8, 1.2)  # Seasonal factor
#         promotion_effect = random.uniform(0.9, 1.3)  # Impact of promotions/discounts
#         economic_factor = random.uniform(0.95, 1.05)  # Macroeconomic conditions
#
#         # Calculate the final predicted demand
#         predicted_demand = int(base_demand * trend * seasonality * promotion_effect * economic_factor)
#
#         # Confidence interval for predicted demand
#         confidence_interval = (predicted_demand - random.randint(10, 20), predicted_demand + random.randint(10, 20))
#
#         # Generate competitor action impact (could be a factor in the confidence interval)
#         competitor_action_impact = random.uniform(0.9, 1.1)
#
#         # Store the data in the predictions dictionary
#         predictions[product] = {
#             'Historical Demand': historical_demand,
#             'Predicted Demand': predicted_demand,
#             'Confidence Interval': confidence_interval,
#             'Trend Factor': trend,
#             'Seasonality Factor': seasonality,
#             'Promotion Effect': promotion_effect,
#             'Economic Factor': economic_factor,
#             'Competitor Action Impact': competitor_action_impact
#         }
#
#     return predictions
#
#
# # Example usage
# # print(generate_demand_forecasting_predictions())
