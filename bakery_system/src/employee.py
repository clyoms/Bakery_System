from typing import Dict, List, Tuple, Optional
from datetime import datetime
from pathlib import Path
import csv

class Employee:
    """
    Class representing an employee at Murphy's Bakery.
    Handles employee data operations and validation.
    Attributes:
        employee_id (str): Unique identifier for the employee
        first_name (str): Employee's first name
        last_name (str): Employee's last name
        position (str): Employee's position in the bakery
        start_date (str): Employee's start date in YYYY-MM-DD format
    """
    def __init__(self, employee_id: str, first_name: str, last_name: str, position: str, start_date: str):
        """
        Initialize an Employee object with the provided attributes.
        """
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.start_date = start_date
        self.employees_file = Path("data/employees.csv")

    @classmethod
    def from_dict(cls, employee_data: Dict[str, str]) -> 'Employee':
        """
        Create an Employee object from a dictionary.
        """
        return cls(
            employee_id=employee_data['id'],
            first_name=employee_data['first_name'],
            last_name=employee_data['last_name'],
            position=employee_data['position'],
            start_date=employee_data['start_date']
        )

    def to_dict(self) -> Dict[str, str]:
        """
        Convert Employee object to a dictionary.
        """
        return {
            'id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
            'start_date': self.start_date
        }

    def validate(self) -> Tuple[bool, str]:
        """
        Validate employee data according to business rules.
        """
        if not all([self.employee_id, self.first_name, self.last_name, self.position, self.start_date]):
            return False, "All fields are required"
        
        try:
            datetime.strptime(self.start_date, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"

        if not (2 <= len(self.first_name) <= 30):
            return False, "First name must be between 2 and 30 characters"
        
        if not (2 <= len(self.last_name) <= 30):
            return False, "Last name must be between 2 and 30 characters"

        return True, ""

    def update_name(self, new_first_name: str, new_last_name: str) -> Tuple[bool, str]:
        """
        Update employee name with validation.
        """
        temp_employee = Employee(
            self.employee_id,
            new_first_name,
            new_last_name,
            self.position,
            self.start_date
        )
        is_valid, error = temp_employee.validate()
        if not is_valid:
            return False, error

        self.first_name = new_first_name
        self.last_name = new_last_name
        return True, ""

    def update_position(self, new_position: str) -> Tuple[bool, str]:
        """
        Update employee position with validation.
        """
        if not new_position:
            return False, "Position cannot be empty"
        
        self.position = new_position
        return True, ""

    def initialize_employee_file(self) -> None:
        if not self.employees_file.exists():
            with self.employees_file.open('w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'first_name', 'last_name', 'position', 'start_date'])

    def load_employees(self) -> Tuple[bool, List[Dict[str, str]], str]:
        try:
            employees = []
            with self.employees_file.open('r', newline='') as f:
                reader = csv.DictReader(f)
                employees = list(reader)
            return True, employees, ""
        except Exception as e:
            return False, [], f"Failed to load employees: {str(e)}"

    def load_employee_by_id(self, employee_id: str) -> Tuple[bool, Optional[Dict[str, str]], str]:
        success, employees, error = self.load_employees()
        if not success:
            return False, None, error
        
        for employee in employees:
            if employee['id'] == employee_id:
                return True, employee, ""
        return False, None, f"Employee with ID {employee_id} not found"

    def save(self) -> Tuple[bool, str]:
        success, employees, error = self.load_employees()
        if not success:
            return False, error

        if any(e['id'] == self.employee_id for e in employees):
            return False, f"Employee with ID {self.employee_id} already exists"

        try:
            with self.employees_file.open('a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'first_name', 'last_name', 'position', 'start_date'])
                writer.writerow(self.to_dict())
            return True, ""
        except Exception as e:
            return False, f"Failed to save employee: {str(e)}"

    def update(self) -> Tuple[bool, str]:
        success, employees, error = self.load_employees()
        if not success:
            return False, error

        updated = False
        for i, emp in enumerate(employees):
            if emp['id'] == self.employee_id:
                employees[i] = self.to_dict()
                updated = True
                break

        if not updated:
            return False, f"Employee with ID {self.employee_id} not found"

        try:
            with self.employees_file.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'first_name', 'last_name', 'position', 'start_date'])
                writer.writeheader()
                writer.writerows(employees)
            return True, ""
        except Exception as e:
            return False, f"Failed to update employee: {str(e)}"

    def delete(self) -> Tuple[bool, str]:
        success, employees, error = self.load_employees()
        if not success:
            return False, error

        original_length = len(employees)
        employees = [emp for emp in employees if emp['id'] != self.employee_id]
        
        if len(employees) == original_length:
            return False, f"Employee with ID {self.employee_id} not found"

        try:
            with self.employees_file.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'first_name', 'last_name', 'position', 'start_date'])
                writer.writeheader()
                writer.writerows(employees)
            return True, ""
        except Exception as e:
            return False, f"Failed to delete employee: {str(e)}"

















































