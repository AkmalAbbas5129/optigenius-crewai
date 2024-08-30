import random


def generate_demand_supply_matching_predictions():
    products = ['Product_A', 'Product_B', 'Product_C', 'Product_D']
    predictions = {}

    for product in products:
        # Generate predicted demand and available supply
        predicted_demand = random.randint(10, 20)
        available_supply = random.randint(10, 20)

        # Ensure supply is enough to handle the demand but add a realistic gap
        if available_supply >= predicted_demand:
            demand_supply_gap = available_supply - predicted_demand
        else:
            demand_supply_gap = predicted_demand - available_supply

        predictions[product] = {
            'Predicted_Demand_In_Units': predicted_demand,
            'Available_Supply_In_Units': available_supply,
            'Demand_Supply_Gap_In_Units': demand_supply_gap
        }

    return predictions


if __name__ == "__main__":
    print(generate_demand_supply_matching_predictions())
