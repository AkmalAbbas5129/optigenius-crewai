import random


def generate_demand_forecasting_predictions():
    products = ['Product_A', 'Product_B', 'Product_C', 'Product_D']
    predictions = {}

    for product in products:
        # Historical demand with a seasonal trend
        historical_demand = [random.randint(80, 200) + 20 * ((i % 12) // 3) for i in range(12)]

        # Predicted demand with a base value, trend, and seasonality
        base_demand = random.randint(100, 250)
        trend = random.uniform(0.9, 1.1)  # Long-term trend factor
        seasonality = random.uniform(0.8, 1.2)  # Seasonal factor
        promotion_effect = random.uniform(0.9, 1.3)  # Impact of promotions/discounts
        economic_factor = random.uniform(0.95, 1.05)  # Macroeconomic conditions

        # Calculate the final predicted demand
        predicted_demand = int(base_demand * trend * seasonality * promotion_effect * economic_factor)

        # Confidence interval for predicted demand
        confidence_interval = (predicted_demand - random.randint(10, 20), predicted_demand + random.randint(10, 20))

        # Generate competitor action impact (could be a factor in the confidence interval)
        competitor_action_impact = random.uniform(0.9, 1.1)

        # Store the data in the predictions dictionary
        predictions[product] = {
            'Historical Demand': historical_demand,
            'Predicted Demand': predicted_demand,
            'Confidence Interval': confidence_interval,
            'Trend Factor': trend,
            'Seasonality Factor': seasonality,
            'Promotion Effect': promotion_effect,
            'Economic Factor': economic_factor,
            'Competitor Action Impact': competitor_action_impact
        }

    return predictions


# Example usage
# print(generate_demand_forecasting_predictions())
