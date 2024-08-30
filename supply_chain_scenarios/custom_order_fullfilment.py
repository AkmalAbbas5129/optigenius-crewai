import random


def generate_random_values(num_products, value_range):
    return [random.randint(value_range[0], value_range[1]) for _ in range(num_products)]


def generate_customer_order_fulfillment_predictions():
    num_products = 2  # Adjust number of products as needed
    order_fulfillment_time_range = (2, 10)  # in days
    order_quantity_range = (5, 20)  # in units
    max_order_capacity_range = (50, 70)  # in units
    available_inventory_range = (100, 110)  # in units

    # Generate predictions
    order_fulfillment_time = generate_random_values(num_products, order_fulfillment_time_range)
    order_quantity = generate_random_values(num_products, order_quantity_range)
    max_order_capacity = generate_random_values(num_products, max_order_capacity_range)
    available_inventory = generate_random_values(num_products, available_inventory_range)

    scenario = "Customer Order Fulfillment Optimization"
    dummy_vars = {
        "order_fulfillment_time_in_days": order_fulfillment_time,
        "order_quantity": order_quantity,
        "max_order_capacity": max_order_capacity,
        "available_inventory": available_inventory
    }

    return dummy_vars

# def generate_random_values_custom_order_fulfillment(min_value, max_value, num_products, seed=None):
#     if seed:
#         random.seed(seed)
#     return {f'Product_{chr(65 + i)}': random.randint(min_value, max_value) for i in range(num_products)}
#
#
# def get_dummy_model_values_custom_order():
#     # Example ranges and number of products
#     num_products = 3
#     order_fulfillment_time_range = (2, 10)  # in days
#     order_quantity_range = (5, 20)  # in units
#     max_order_capacity_range = (50, 70)  # in units
#     available_inventory_range = (100, 110)  # in units
#
#     # Generate predictions
#     order_fulfillment_time = generate_random_values_custom_order_fulfillment(*order_fulfillment_time_range,
#                                                                              num_products)
#     order_quantity = generate_random_values_custom_order_fulfillment(*order_quantity_range, num_products)
#     max_order_capacity = generate_random_values_custom_order_fulfillment(*max_order_capacity_range, num_products)
#     available_inventory = generate_random_values_custom_order_fulfillment(*available_inventory_range, num_products)
#     scenario = "Customer Order Fulfillment Optimization"
#     dummy_vars = {
#         "order_fullfillment_time_in_days": order_fulfillment_time,
#         "order_quantity": order_quantity,
#         "max_order_capacity": max_order_capacity,
#         "available_inventory": available_inventory
#     }
#
#     return dummy_vars
