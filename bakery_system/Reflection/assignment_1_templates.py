# assignment_1_templates.py

from pathlib import Path
import csv
from datetime import datetime

def initialize_data_directory(data_dir: str = "data") -> tuple[bool, str]:
    """
    Initialize a directory for storing data files.
    Creates the directory if it doesn't exist.
    
    Args:
        data_dir (str): Name of the directory to create/check. Defaults to "data"
        
    Returns:
        tuple[bool, str]: (Success status, Error message if failed or empty string if successful)
        
    Member 1 Name: Chulainn
    Student ID: 124357031
    
    Member 3 Name: Darragh
    Student ID: 124496482
    """
    pass

def validate_text_field(field_name: str, value: str, max_length: int = 30) -> tuple[bool, str]:
    """
    Validate a text field according to specified rules.
    
    Args:
        field_name (str): Name of the field being validated (for error messages)
        value (str): The text value to validate
        max_length (int): Maximum allowed length of the text. Defaults to 30
        
    Returns:
        tuple[bool, str]: (Validation status, Error message if invalid or empty string if valid)
        
    Member 2 Name: Barry
    Student ID: 124352611
    Member 4 Name: George
    Student ID: 124455426
    """
    pass

def add_employee(first_name: str, last_name: str, position: str, start_date: str) -> tuple[bool, str]:
    """
    Create a new employee record in employees.csv.
    Validates input data and generates unique employee ID.
    
    Member 1 Name: Chulainn
    Student ID: 124357031
    """
    pass

def get_employee_by_id(employee_id: str) -> tuple[bool, dict | str]:
    """
    Retrieve employee record by ID.
    Handles file reading and error cases for missing records.
    
    Member 2 Name: Barry
    Student ID: 124352611
    """
    pass

def update_employee_name(employee_id: str, new_first_name: str, new_last_name: str) -> tuple[bool, str]:
    """
    Update employee's name while maintaining other data.
    Must read file, update specific record, and write back safely.
    
    Member 3 Name: Darragh
    Student ID: 124496482
    """
    pass

def delete_employee(employee_id: str) -> tuple[bool, str]:
    """
    Remove employee record while maintaining file integrity.
    Should verify record exists before attempting deletion.
    
    Member 4 Name: George
    Student ID: 124455426
    """
    pass

# wage_rates.py
def add_position_rate(position: str, base_rate: float, weekend_rate: float) -> tuple[bool, str]:
    """
    Add new position with wage rates to wage_rates.json.
    Validates rates and ensures position doesn't already exist.
    
    Member 4 Name: George
    Student ID: 124455426
    """
    pass

def get_position_rate(position: str) -> tuple[bool, dict | str]:
    """
    Get wage rates for a specific position.
    Handles JSON reading and missing position cases.
    
    Member 3 Name: Darragh
    Student ID: 124496482
    """
    pass

def update_position_rate(position: str, new_base_rate: float, new_weekend_rate: float) -> tuple[bool, str]:
    """
    Update rates for an existing position.
    Must validate new rates before updating.
    
    Member 2 Name: Barry
    Student ID: 124352611
    """
    pass

def delete_position_rate(position: str) -> tuple[bool, str]:
    """
    Remove a position and its rates.
    Should check for employees in this position before deletion.
    
    Member 1 Name: Chulainn
    Student ID: 124357031
    """
    pass
