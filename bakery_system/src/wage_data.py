import json
from pathlib import Path

# Use relative path
WAGE_FILE = Path("data/wage_rates.json")

# Ensure the wage data file exists
def initialize_wage_file():
    default_wage_data = {
        "Head Baker": {"base_rate": 18.50, "weekend_rate": 22.00},
        "Baker": {"base_rate": 16.00, "weekend_rate": 19.00},
        "Pastry Chef": {"base_rate": 16.50, "weekend_rate": 19.50},
        "Counter Staff": {"base_rate": 14.00, "weekend_rate": 16.50},
        "Kitchen Assistant": {"base_rate": 13.50, "weekend_rate": 16.00}
    }

    if not WAGE_FILE.exists():
        with WAGE_FILE.open(mode='w') as file:
            json.dump(default_wage_data, file, indent=4)

# Validate that the rate is a positive number
def validate_rate(rate):
    if rate <= 0:
        raise ValueError("Rate must be a positive number.")

# Add a new position pay rate to the JSON file
def add_position_rate(position, base_rate, weekend_rate):
    validate_rate(base_rate)
    validate_rate(weekend_rate)
    
    with WAGE_FILE.open(mode='r') as file:
        wage_data = json.load(file)
    
    if position in wage_data:
        raise ValueError(f"Position '{position}' already exists.")
    
    wage_data[position] = {'base_rate': base_rate, 'weekend_rate': weekend_rate}
    
    with WAGE_FILE.open(mode='w') as file:
        json.dump(wage_data, file, indent=4)

# Get the pay rate for a specific position
def get_position_rate(position):
    with WAGE_FILE.open(mode='r') as file:
        wage_data = json.load(file)
    
    return wage_data.get(position, None)

# Update the pay rates for a specific position
def update_position_rate(position, new_base_rate, new_weekend_rate):
    validate_rate(new_base_rate)
    validate_rate(new_weekend_rate)
    
    with WAGE_FILE.open(mode='r') as file:
        wage_data = json.load(file)
    
    if position not in wage_data:
        raise ValueError(f"Position '{position}' not found.")
    
    wage_data[position] = {'base_rate': new_base_rate, 'weekend_rate': new_weekend_rate}
    
    with WAGE_FILE.open(mode='w') as file:
        json.dump(wage_data, file, indent=4)

# Delete a position from the wage data file
def delete_position_rate(position):
    with WAGE_FILE.open(mode='r') as file:
        wage_data = json.load(file)
    
    if position not in wage_data:
        raise ValueError(f"Position '{position}' not found.")
    
    del wage_data[position]
    
    with WAGE_FILE.open(mode='w') as file:
        json.dump(wage_data, file, indent=4)
