from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union, Any
from pathlib import Path

class Employee:
    def __init__(self, employee_id: str, first_name: str, last_name: str, position: str, start_date: str):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.start_date = start_date

    @classmethod
    def from_dict(cls, employee_data: Dict[str, str]) -> 'Employee':
        return cls(
            employee_id=employee_data['id'],
            first_name=employee_data['first_name'],
            last_name=employee_data['last_name'],
            position=employee_data['position'],
            start_date=employee_data['start_date']
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            'id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
            'start_date': self.start_date
        }

    def validate(self) -> Tuple[bool, str]:
        if not all([self.employee_id, self.first_name, self.last_name, self.position, self.start_date]):
            return False, "All fields are required"
        
        try:
            datetime.strptime(self.start_date, '%d-%m-%Y')
        except ValueError:
            return False, "Invalid date format. Use DD-MM-YYYY"
            
        return True, ""

    def update_name(self, new_first_name: str, new_last_name: str) -> Tuple[bool, str]:
        if not new_first_name or not new_last_name:
            return False, "Both first and last names are required"
        
        self.first_name = new_first_name
        self.last_name = new_last_name
        return True, ""

    def update_position(self, new_position: str) -> Tuple[bool, str]:
        if not new_position:
            return False, "Position cannot be empty"
        
        self.position = new_position
        return True, ""


