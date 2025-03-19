from typing import Dict, Tuple
from datetime import datetime
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

















































