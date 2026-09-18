import math
from .fuel_service import FUEL_DF

VEHICLE_RANGE_MILES = 500.0
MPG = 10.0

def calculate_optimal_fuel_stops(distance_miles):
    """
    Calculates the required fuel, number of stops, and the optimal (cheapest)
    truck stops to use based on the vehicle's 500-mile range constraint.
    """
    # 1. Calculate base fuel requirements
    gallons_needed = distance_miles / MPG
    
    # 2. Calculate how many stops we MUST make before running out of fuel
    # If trip is 1200 miles, we need stops at ~500 and ~1000 miles (2 stops)
    num_stops_required = math.floor(distance_miles / VEHICLE_RANGE_MILES)
    
    stops_list = []
    total_cost = 0.0

    if FUEL_DF.empty:
        raise Exception("Fuel data is not loaded. Cannot calculate cost.")

    # 3. Greedy Optimization: Find the absolute cheapest stops in our dataset
    # We sort the pandas DataFrame by price and pick the cheapest ones.
    cheapest_stops = FUEL_DF.sort_values(by='Retail Price').head(max(1, num_stops_required))
    
    for index, row in cheapest_stops.iterrows():
        stops_list.append({
            "truckstop_name": row['Truckstop Name'],
            "address": row['Address'],
            "city_state": f"{row['City']}, {row['State']}",
            "price_per_gallon": row['Retail Price']
        })

    # 4. Calculate total cost using the average price of our selected optimal stops
    avg_optimal_price = cheapest_stops['Retail Price'].mean()
    total_cost = gallons_needed * avg_optimal_price

    return {
        "total_gallons_used": round(gallons_needed, 2),
        "total_fuel_cost_usd": round(total_cost, 2),
        "num_stops_required": num_stops_required,
        "recommended_fuel_stops": stops_list
    }