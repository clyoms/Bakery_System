import csv
from pathlib import Path
from datetime import datetime
from tabulate import tabulate

# Define the employee data file path - Using pathlib
EMPLOYEE_FILE = Path('data/employees.csv')

def initialize_employee_file():
    """Ensures employees.csv exists and contains a valid header."""
    EMPLOYEE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    file_exists = EMPLOYEE_FILE.exists()
    
    with EMPLOYEE_FILE.open(mode='r+', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        first_line = next(reader, None)
        
        # If the file is empty or missing headers, write them
        if first_line != ['id', 'first_name', 'last_name', 'position', 'start_date']:
            file.seek(0)  # Move to the start of the file
            writer = csv.writer(file)
            writer.writerow(['id', 'first_name', 'last_name', 'position', 'start_date'])

def validate_text_field(field_name, value, max_length=30):
    """Validates text fields (first name, last name, position)."""
    if not value or len(value) > max_length:
        raise ValueError(f"{field_name} must not be empty and should not exceed {max_length} characters.")

def validate_date_format(date_str):
    """Validates date format (DD-MM-YYYY)."""
    try:
        datetime.strptime(date_str, '%d-%m-%Y')
        return True
    except ValueError:
        raise ValueError("Invalid date format. Please use DD-MM-YYYY.")

def generate_employee_id():
    """Generates the next employee ID (E001, E002, etc.)."""
    if not EMPLOYEE_FILE.exists():
        return "E001"
    
    try:
        with EMPLOYEE_FILE.open(mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            employee_ids = [row[0] for row in reader if row]
        
        if not employee_ids:
            return "E001"
        
        last_id = employee_ids[-1]
        last_number = int(last_id[1:])
        return f"E{last_number + 1:03d}"
    except Exception as e:
        print(f"Error generating ID: {e}")
        return "E001"

def add_employee(first_name, last_name, position, start_date):
    """Adds a new employee to the CSV file."""
    validate_text_field("First name", first_name)
    validate_text_field("Last name", last_name)
    validate_text_field("Position", position)
    validate_date_format(start_date)
    
    # Ensure the file has headers before appending data
    initialize_employee_file()
    
    employee_id = generate_employee_id()
    with EMPLOYEE_FILE.open(mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow([employee_id, first_name, last_name, position, start_date])

def get_employee_by_id(employee_id):
    """Retrieves employee details by ID."""
    try:
        with EMPLOYEE_FILE.open(mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row and row[0] == employee_id:
                    return row
        return None
    except Exception as e:
        print(f"Error reading employee: {e}")
        return None

def update_employee_name(employee_id, new_first_name, new_last_name):
    """Updates an employee's first and last name."""
    validate_text_field("First name", new_first_name)
    validate_text_field("Last name", new_last_name)
    
    employees = []
    updated = False
    
    with EMPLOYEE_FILE.open(mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        header = next(reader)
        employees.append(header)
        for row in reader:
            if row and row[0] == employee_id:
                row[1] = new_first_name
                row[2] = new_last_name
                updated = True
            employees.append(row)
    
    if updated:
        with EMPLOYEE_FILE.open(mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerows(employees)
    else:
        raise ValueError("Employee ID not found.")

def delete_employee(employee_id):
    """Deletes an employee from the CSV file."""
    employees = []
    deleted = False
    
    with EMPLOYEE_FILE.open(mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        header = next(reader)
        employees.append(header)
        for row in reader:
            if row and row[0] != employee_id:
                employees.append(row)
            elif row:
                deleted = True
    
    if deleted:
        with EMPLOYEE_FILE.open(mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerows(employees)
    else:
        raise ValueError("Employee ID not found.")

def print_employee_data():
    """Prints the employee data in a tabulated format."""
    with EMPLOYEE_FILE.open(mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        data = list(reader)
    
    print(tabulate(data, headers="firstrow", tablefmt="grid"))
