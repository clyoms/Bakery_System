from datetime import datetime
from typing import Optional, Dict, Tuple

class Employee:
    def __init__(self, emp_id: Optional[str], first_name: str, last_name: str, position: str, start_date: str):
        self.staff_id = emp_id
        self.fname = first_name
        self.lname = last_name
        self.job = position
        self.start_date = start_date

    @classmethod
    def validate_name(cls, name: str) -> Tuple[bool, str]:
        """Validate employee name"""
        if not name or not name.strip():
            return False, "Name cannot be empty"
        if not all(c.isalpha() or c.isspace() for c in name):
            return False, "Name can only contain letters and spaces"
        if len(name) > 30:
            return False, "Name must be less than 30 characters"
        return True, ""

    @classmethod
    def validate_date(cls, date_str: str) -> Tuple[bool, str]:
        """Validate date format (DD-MM-YYYY)"""
        try:
            datetime.strptime(date_str, '%d-%m-%Y')
            return True, ""
        except ValueError:
            return False, "Invalid date format. Use DD-MM-YYYY"

    def validate(self) -> Tuple[bool, str]:
        """Validate all employee data"""
        # Validate first name
        name_valid, name_msg = self.validate_name(self.fname)
        if not name_valid:
            return False, f"Invalid first name: {name_msg}"

        # Validate last name
        name_valid, name_msg = self.validate_name(self.lname)
        if not name_valid:
            return False, f"Invalid last name: {name_msg}"

        # Validate date
        date_valid, date_msg = self.validate_date(self.start_date)
        if not date_valid:
            return False, date_msg

        # Validate position
        if not self.job:
            return False, "Position cannot be empty"

        return True, ""

    def to_dict(self) -> Dict[str, str]:
        """Convert employee object to dictionary for storage"""
        return {
            'staff_id': self.staff_id,
            'fname': self.fname,
            'lname': self.lname,
            'job': self.job,
            'start': self.start_date
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Employee':
        """Create employee object from dictionary data"""
        return cls(
            data['staff_id'],
            data['fname'],
            data['lname'],
            data['job'],
            data['start']
        )

    def calculate_tenure(self) -> int:
        """Calculate employee tenure in days"""
        start = datetime.strptime(self.start_date, '%d-%m-%Y')
        return (datetime.now() - start).days

    def update_name(self, new_first_name: str, new_last_name: str) -> Tuple[bool, str]:
        """Update employee name with validation"""
        if new_first_name:
            valid, msg = self.validate_name(new_first_name)
            if not valid:
                return False, f"Invalid first name: {msg}"
            self.fname = new_first_name

        if new_last_name:
            valid, msg = self.validate_name(new_last_name)
            if not valid:
                return False, f"Invalid last name: {msg}"
            self.lname = new_last_name

        return True, "Name updated successfully"

    def update_position(self, new_position: str) -> Tuple[bool, str]:
        """Update employee position with validation"""
        if not new_position:
            return False, "Position cannot be empty"
        self.job = new_position
        return True, "Position updated successfully"
