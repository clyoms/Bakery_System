import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from .employee import Employee
from .schedule import Schedule

class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.employees_file = self.data_dir / "employees.csv"
        self.schedules_file = self.data_dir / "schedules.csv"
        self.wage_rates_file = self.data_dir / "wage_rates.json"

    def initialize_data_directory(self) -> Tuple[bool, str]:
        try:
            self.data_dir.mkdir(exist_ok=True)
            
            # Create empty files if they don't exist
            if not self.employees_file.exists():
                self._create_employees_file()
            if not self.schedules_file.exists():
                self._create_schedules_file()
            if not self.wage_rates_file.exists():
                self._create_wage_rates_file()
                
            return True, ""
        except Exception as e:
            return False, f"Failed to initialize data directory: {str(e)}"

    def _create_employees_file(self):
        with self.employees_file.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'first_name', 'last_name', 'position', 'start_date'])

    def _create_schedules_file(self):
        with self.schedules_file.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['schedule_id', 'employee_id', 'week_start_date', 
                           'mon_hours', 'tue_hours', 'wed_hours', 'thu_hours', 
                           'fri_hours', 'sat_hours', 'sun_hours', 'total_hours', 'total_pay'])

    def _create_wage_rates_file(self):
        default_rates = {
            "Baker": {"base_rate": 16.00, "weekend_rate": 19.00},
            "Counter Staff": {"base_rate": 14.00, "weekend_rate": 16.50}
        }
        with self.wage_rates_file.open('w') as f:
            json.dump(default_rates, f, indent=4)

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

    def save_employee(self, employee: Employee) -> Tuple[bool, str]:
        success, employees, error = self.load_employees()
        if not success:
            return False, error

        # Check if employee ID already exists
        if any(e['id'] == employee.employee_id for e in employees):
            return False, f"Employee with ID {employee.employee_id} already exists"

        try:
            with self.employees_file.open('a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'first_name', 'last_name', 'position', 'start_date'])
                writer.writerow(employee.to_dict())
            return True, ""
        except Exception as e:
            return False, f"Failed to save employee: {str(e)}"

    def update_employee(self, employee: Employee) -> Tuple[bool, str]:
        success, employees, error = self.load_employees()
        if not success:
            return False, error

        updated = False
        for i, emp in enumerate(employees):
            if emp['id'] == employee.employee_id:
                employees[i] = employee.to_dict()
                updated = True
                break

        if not updated:
            return False, f"Employee with ID {employee.employee_id} not found"

        try:
            with self.employees_file.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'first_name', 'last_name', 'position', 'start_date'])
                writer.writeheader()
                writer.writerows(employees)
            return True, ""
        except Exception as e:
            return False, f"Failed to update employee: {str(e)}"

    def delete_employee(self, employee_id: str) -> Tuple[bool, str]:
        success, employees, error = self.load_employees()
        if not success:
            return False, error

        original_length = len(employees)
        employees = [emp for emp in employees if emp['id'] != employee_id]
        
        if len(employees) == original_length:
            return False, f"Employee with ID {employee_id} not found"

        try:
            with self.employees_file.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'first_name', 'last_name', 'position', 'start_date'])
                writer.writeheader()
                writer.writerows(employees)
            return True, ""
        except Exception as e:
            return False, f"Failed to delete employee: {str(e)}"

    def load_wage_rates(self) -> Tuple[bool, Dict[str, Dict[str, float]], str]:
        try:
            with self.wage_rates_file.open('r') as f:
                wage_rates = json.load(f)
            return True, wage_rates, ""
        except Exception as e:
            return False, {}, f"Failed to load wage rates: {str(e)}"

    def save_wage_rates(self, wage_rates: Dict[str, Dict[str, float]]) -> Tuple[bool, str]:
        try:
            with self.wage_rates_file.open('w') as f:
                json.dump(wage_rates, f, indent=4)
            return True, ""
        except Exception as e:
            return False, f"Failed to save wage rates: {str(e)}"

    def get_position_rate(self, position: str) -> Tuple[bool, Optional[Dict[str, float]], str]:
        success, wage_rates, error = self.load_wage_rates()
        if not success:
            return False, None, error
        
        if position not in wage_rates:
            return False, None, f"Position '{position}' not found"
        
        return True, wage_rates[position], ""

    def update_position_rate(self, position: str, base_rate: float, weekend_rate: float) -> Tuple[bool, str]:
        success, wage_rates, error = self.load_wage_rates()
        if not success:
            return False, error
        
        if position not in wage_rates:
            return False, f"Position '{position}' not found"
        
        wage_rates[position] = {
            "base_rate": base_rate,
            "weekend_rate": weekend_rate
        }
        
        return self.save_wage_rates(wage_rates)

    def add_position_rate(self, position: str, base_rate: float, weekend_rate: float) -> Tuple[bool, str]:
        success, wage_rates, error = self.load_wage_rates()
        if not success:
            return False, error
        
        if position in wage_rates:
            return False, f"Position '{position}' already exists"
        
        wage_rates[position] = {
            "base_rate": base_rate,
            "weekend_rate": weekend_rate
        }
        
        return self.save_wage_rates(wage_rates)

    def delete_position_rate(self, position: str) -> Tuple[bool, str]:
        success, wage_rates, error = self.load_wage_rates()
        if not success:
            return False, error
        
        if position not in wage_rates:
            return False, f"Position '{position}' not found"
        
        del wage_rates[position]
        return self.save_wage_rates(wage_rates)

