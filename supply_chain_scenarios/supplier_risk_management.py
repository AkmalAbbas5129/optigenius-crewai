import random


def generate_supplier_risk_predictions():
    # List of suppliers
    suppliers = ['Supplier A', 'Supplier B', 'Supplier C']

    # Dictionary to store predictions for each supplier
    predictions = {}

    for supplier in suppliers:
        # Risk Score: Simulates the risk associated with the supplier.
        # Lower values indicate lower risk and higher values indicate higher risk.
        risk_score = random.uniform(0.2, 0.8)  # Realistic risk scores between 0.2 and 0.8

        # Predicted Delays: Simulates potential delays in days.
        # This reflects how often suppliers may delay their deliveries.
        predicted_delays = random.randint(1, 7)  # Realistic delays between 1 and 7 days

        # Cost Variability: Represents how much the supplier's costs might fluctuate.
        # A lower percentage indicates less fluctuation.
        cost_variability = random.uniform(0.05, 0.15)  # Realistic cost variability between 5% and 15%

        # Store the generated values in the predictions dictionary
        predictions[supplier] = {
            'Risk Score': risk_score,
            'Predicted_Delays_In_Days': predicted_delays,
            'Cost_Variability_In_Percentage': cost_variability
        }

    # Return the dictionary containing predictions for all suppliers
    return predictions


if __name__ == "__main__":
    print(generate_supplier_risk_predictions())
