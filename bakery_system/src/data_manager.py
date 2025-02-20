import csv
import json
import os

# Directory for data files (use relative path if files are in the same project folder)
DATA_DIR = "C:\\Users\\chula\\Downloads\\bakery_system\\data"


# Create easy to use file paths
EMPLOYEES_FILE = os.path.join(DATA_DIR, "employees.csv")
SCHEDULES_FILE = os.path.join(DATA_DIR, "schedules.csv")
WAGE_RATES_FILE = os.path.join(DATA_DIR, "wage_rates.json")

# Function to check if a file exists and is accessible
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return False
    return True

# Function to read CSV files
def read_employees():
    if check_file_exists(EMPLOYEES_FILE):
        try:
            with open(EMPLOYEES_FILE, mode='r', newline='') as file:
                return list(csv.DictReader(file))
        except Exception as e:
            print(f"Error reading employees.csv: {e}")
            return []
    return []

def read_schedules():
    if check_file_exists(SCHEDULES_FILE):
        try:
            with open(SCHEDULES_FILE, mode='r', newline='') as file:
                return list(csv.DictReader(file))
        except Exception as e:
            print(f"Error reading schedules.csv: {e}")
            return []
    return []

# Function to write data to CSV files
def write_employees(data):
    fieldnames = ["id", "last_name", "first_name", "position", "start_date"]
    try:
        with open(EMPLOYEES_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Error writing to employees.csv: {e}")

def write_schedules(data):
    fieldnames = ["schedule_id", "employee_id", "week_start_date", "mon_hours", 
                  "tue_hours", "wed_hours", "thu_hours", "fri_hours", 
                  "sat_hours", "sun_hours", "total_pay"]
    try:
        with open(SCHEDULES_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Error writing to schedules.csv: {e}")

# Function to read JSON files
def read_wage_rates():
    if check_file_exists(WAGE_RATES_FILE):
        try:
            with open(WAGE_RATES_FILE, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading wage_rates.json: {e}")
            return {}
    return {}

# Function to write JSON files
def write_wage_rates(data):
    try:
        with open(WAGE_RATES_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error writing to wage_rates.json: {e}")

# Example usage
employees_data = read_employees()
schedules_data = read_schedules()
wage_rates_data = read_wage_rates()

# Debugging the directory
print(f"Employees file exists: {os.path.exists(EMPLOYEES_FILE)}")
print(f"Schedules file exists: {os.path.exists(SCHEDULES_FILE)}")
print(f"Wage rates file exists: {os.path.exists(WAGE_RATES_FILE)}")

print(f"Current working directory: {os.getcwd()}")

