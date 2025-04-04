from pathlib import Path
import json
import csv
from typing import Tuple, List, Dict, Any, Optional
from datetime import datetime
from employee import Employee
from wage_data import WageManager

class DataManager:
    def __init__(self, data_folder: str = "data"):
        self.data_folder = Path(data_folder)
        self.pay_rates_file = self.data_folder / "wage_rates.json"
        self.schedules_file = self.data_folder / "schedules.csv"
        self.staff_file = self.data_folder / "employees.csv"
        self.reports_folder = self.data_folder / "reports"
        self.wage_manager = WageManager()

    def setup_data_folder(self) -> Tuple[bool, str]:
        """Initialize all necessary data directories and files"""
        try:
            # Create main data folder and reports subfolder
            self.data_folder.mkdir(exist_ok=True)
            self.reports_folder.mkdir(exist_ok=True)

            # Initialize files if they don't exist
            if not self.pay_rates_file.exists():
                self._create_pay_rates()
            if not self.schedules_file.exists():
                self._create_schedules_file()
            if not self.staff_file.exists():
                self._create_staff_file()

            return True, ""
        except Exception as e:
            return False, f"Couldn't set up data folder: {str(e)}"

    def _create_staff_file(self) -> None:
        """Create initial staff CSV file with headers"""
        headers = ['staff_id', 'fname', 'lname', 'job', 'start']
        with self.staff_file.open('w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def _create_pay_rates(self) -> None:
        """Create initial wage rates file"""
        default_rates = {
            "Head Baker": {"base_rate": 18.50, "weekend_rate": 22.00},
            "Baker": {"base_rate": 16.00, "weekend_rate": 19.00},
            "Pastry Chef": {"base_rate": 16.50, "weekend_rate": 19.50},
            "Counter Staff": {"base_rate": 14.00, "weekend_rate": 16.50},
            "Kitchen Assistant": {"base_rate": 13.50, "weekend_rate": 16.00}
        }
        with self.pay_rates_file.open('w') as f:
            json.dump(default_rates, f, indent=4)

    # Wage rate operations
    def get_wage_rate(self, position: str, is_weekend: bool = False) -> Optional[float]:
        """Get wage rate for a position"""
        try:
            with self.pay_rates_file.open('r') as f:
                rates = json.load(f)
                for stored_title, rate_info in rates.items():
                    if stored_title.lower() == position.lower():
                        return rate_info['weekend_rate'] if is_weekend else rate_info['base_rate']
            return None
        except Exception:
            return None

    def add_wage_rate(self, position: str, base_rate: float, weekend_rate: float) -> Tuple[bool, str]:
        """Add new wage rate"""
        try:
            # Validate rates
            valid, msg = self.wage_manager.validate_rate(base_rate, "base rate")
            if not valid:
                return False, msg

            valid, msg = self.wage_manager.validate_rate(weekend_rate, "weekend rate")
            if not valid:
                return False, msg

            with self.pay_rates_file.open('r') as f:
                rates = json.load(f)

            if position.lower() in [k.lower() for k in rates.keys()]:
                return False, f"Position '{position}' already exists"

            rates[position] = {'base_rate': base_rate, 'weekend_rate': weekend_rate}

            with self.pay_rates_file.open('w') as f:
                json.dump(rates, f, indent=4)

            return True, "Wage rate added successfully"
        except Exception as e:
            return False, str(e)

    def get_wage_rates(self) -> Tuple[bool, Dict[str, Dict[str, float]], str]:
        """Get all wage rates"""
        try:
            if not self.pay_rates_file.exists():
                return False, {}, "Wage rates file does not exist"

            with self.pay_rates_file.open('r') as f:
                rates = json.load(f)

            return True, rates, ""
        except Exception as e:
            return False, {}, f"Error loading wage rates: {str(e)}"

    def update_wage_rate(self, position: str, base_rate: float, weekend_rate: float) -> Tuple[bool, str]:
        """Update existing wage rate"""
        try:
            # Validate rates
            valid, msg = self.wage_manager.validate_rate(base_rate, "base rate")
            if not valid:
                return False, msg

            valid, msg = self.wage_manager.validate_rate(weekend_rate, "weekend rate")
            if not valid:
                return False, msg

            with self.pay_rates_file.open('r') as f:
                rates = json.load(f)

            found = False
            for stored_title in list(rates.keys()):
                if stored_title.lower() == position.lower():
                    rates[stored_title] = {
                        'base_rate': base_rate,
                        'weekend_rate': weekend_rate
                    }
                    found = True
                    break

            if not found:
                return False, f"Position '{position}' not found"

            with self.pay_rates_file.open('w') as f:
                json.dump(rates, f, indent=4)

            return True, "Wage rate updated successfully"
        except Exception as e:
            return False, str(e)

    # Employee operations
    def generate_employee_id(self) -> str:
        """Generate a unique employee ID"""
        try:
            if not self.staff_file.exists():
                return "E001"

            with self.staff_file.open(mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                next(reader)  # skip header
                staff_ids = [row[0] for row in reader if row]

            if not staff_ids:
                return "E001"

            # Find the highest ID number by checking all IDs
            highest_num = 0
            for staff_id in staff_ids:
                if staff_id.startswith('E'):
                    try:
                        id_num = int(staff_id[1:])
                        highest_num = max(highest_num, id_num)
                    except ValueError:
                        # Skip IDs that don't follow the expected format
                        continue

            return f"E{highest_num + 1:03d}"
        except Exception as e:
            print(f"Problem making ID: {e}")
            return "E001"

    def add_employee(self, fname: str, lname: str, job: str, start_date: str) -> Tuple[bool, str]:
        """Add new employee"""
        try:
            # Create employee object
            employee = Employee(None, fname, lname, job, start_date)

            # Validate employee data
            valid, msg = employee.validate()
            if not valid:
                return False, msg

            # Generate ID
            employee.staff_id = self.generate_employee_id()

            # Save to file
            with self.staff_file.open('a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    employee.staff_id,
                    employee.fname,
                    employee.lname,
                    employee.job,
                    employee.start_date
                ])

            return True, f"Employee added successfully with ID: {employee.staff_id}"
        except Exception as e:
            return False, f"Error adding employee: {str(e)}"

    def get_employee(self, employee_id: str) -> Tuple[bool, Optional[Dict[str, str]], str]:
        """Get employee by ID"""
        try:
            if not self.staff_file.exists():
                return False, None, "Employee file does not exist"

            with self.staff_file.open(mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for employee in reader:
                    if employee['staff_id'] == employee_id:
                        return True, employee, ""
            return False, None, "Employee not found"
        except Exception as e:
            return False, None, f"Error finding employee: {str(e)}"

    def update_employee(self, employee_id: str, new_fname: str = None, new_lname: str = None, new_job: str = None) -> Tuple[bool, str]:
        """Update employee information"""
        try:
            # Get the employee
            success, employee_data, error = self.get_employee(employee_id)
            if not success:
                return False, error

            # Create employee object
            employee = Employee.from_dict(employee_data)

            # Update fields
            if new_fname or new_lname:
                success, msg = employee.update_name(new_fname, new_lname)
                if not success:
                    return False, msg

            if new_job:
                success, msg = employee.update_position(new_job)
                if not success:
                    return False, msg

            # Save all employees
            success, employees, error = self.get_all_employees()
            if not success:
                return False, error

            # Replace the updated employee
            for i, emp in enumerate(employees):
                if emp['staff_id'] == employee_id:
                    employees[i] = employee.to_dict()
                    break

            # Write back to file
            return self.save_employees(employees)
        except Exception as e:
            return False, f"Error updating employee: {str(e)}"

    def delete_employee(self, employee_id: str) -> Tuple[bool, str]:
        """Delete employee by ID"""
        try:
            # Get all employees
            success, employees, error = self.get_all_employees()
            if not success:
                return False, error

            # Filter out the employee to delete
            original_count = len(employees)
            employees = [emp for emp in employees if emp['staff_id'] != employee_id]

            if len(employees) == original_count:
                return False, f"Employee with ID {employee_id} not found"

            # Write back to file
            return self.save_employees(employees)
        except Exception as e:
            return False, f"Error deleting employee: {str(e)}"

    def get_all_employees(self) -> Tuple[bool, List[Dict[str, str]], str]:
        """Get all employees"""
        try:
            if not self.staff_file.exists():
                return True, [], ""

            employees = []
            with self.staff_file.open(mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    employees.append(row)
            return True, employees, ""
        except Exception as e:
            return False, [], f"Error getting employees: {str(e)}"

    def save_employees(self, employees: List[Dict[str, str]]) -> Tuple[bool, str]:
        """Save employees to file"""
        try:
            headers = ['staff_id', 'fname', 'lname', 'job', 'start']
            with self.staff_file.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(employees)
            return True, "Employees saved successfully"
        except Exception as e:
            return False, f"Error saving employees: {str(e)}"

    def _create_schedules_file(self) -> None:
        """Create initial schedules CSV file with headers"""
        headers = [
            'schedule_id', 'employee_id', 'week_start',
            'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
            'total_hours', 'total_pay'
        ]
        with self.schedules_file.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def save_schedule(self, schedule_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Save schedule to CSV file"""
        try:
            # Ensure week_start is in DD-MM-YYYY format
            try:
                date = datetime.strptime(schedule_data['week_start'], '%Y-%m-%d')
                schedule_data['week_start'] = date.strftime('%d-%m-%Y')
            except ValueError:
                # If already in DD-MM-YYYY format, validate it
                datetime.strptime(schedule_data['week_start'], '%d-%m-%Y')

            # Calculate total hours and pay
            hours = {
                'mon': float(schedule_data.get('mon', 0)),
                'tue': float(schedule_data.get('tue', 0)),
                'wed': float(schedule_data.get('wed', 0)),
                'thu': float(schedule_data.get('thu', 0)),
                'fri': float(schedule_data.get('fri', 0)),
                'sat': float(schedule_data.get('sat', 0)),
                'sun': float(schedule_data.get('sun', 0))
            }

            total_hours = sum(hours.values())
            schedule_data['total_hours'] = total_hours

            # Get employee position for wage calculation
            success, employee, error = self.get_employee(schedule_data['employee_id'])
            if not success:
                return False, f"Failed to get employee details: {error}"

            # Calculate total pay
            success, wage_rates, error = self.get_wage_rates()
            if not success:
                return False, f"Failed to get wage rates: {error}"

            success, total_pay, error = self.wage_manager.calculate_pay(
                employee['job'], hours, wage_rates
            )
            if not success:
                return False, error

            schedule_data['total_pay'] = total_pay

            # Save to CSV
            with self.schedules_file.open('a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=self.schedule_fields)
                writer.writerow(schedule_data)

            return True, "Schedule saved successfully"
        except Exception as e:
            return False, str(e)

    def get_schedules(self, employee_id: str = None, start_date: str = None, end_date: str = None) -> Tuple[bool, List[Dict[str, Any]], str]:
        """Get schedules with optional filtering"""
        try:
            schedules = []
            with self.schedules_file.open('r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Filter by employee if specified
                    if employee_id and row['employee_id'] != employee_id:
                        continue

                    if start_date or end_date:
                        try:
                            # Convert schedule date to datetime object
                            schedule_date = datetime.strptime(row['week_start'], '%d-%m-%Y')

                            if start_date:
                                start = datetime.strptime(start_date, '%d-%m-%Y')
                                if schedule_date < start:
                                    continue

                            if end_date:
                                end = datetime.strptime(end_date, '%d-%m-%Y')
                                if schedule_date > end:
                                    continue
                        except ValueError:
                            # Skip rows with invalid dates
                            continue

                    schedules.append(row)

            return True, schedules, ""
        except Exception as e:
            return False, [], f"Failed to retrieve schedules: {str(e)}"


    def load_schedules_by_employee_id(self, employee_id: str) -> Tuple[bool, List[Dict[str, Any]], str]:
        """Load all schedules for a specific employee"""
        return self.get_schedules(employee_id=employee_id)

    def delete_schedule(self, schedule_id: str) -> Tuple[bool, str]:
        """Delete a schedule by ID"""
        try:
            if not self.schedules_file.exists():
                return False, "No schedules file exists"

            # Read all schedules
            schedules = []
            found = False

            with self.schedules_file.open('r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames

                for row in reader:
                    if row['schedule_id'] != schedule_id:
                        schedules.append(row)
                    else:
                        found = True

            if not found:
                return False, f"Schedule with ID {schedule_id} not found"

            # Write back all schedules except the deleted one
            with self.schedules_file.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(schedules)

            return True, "Schedule deleted successfully"
        except Exception as e:
            return False, f"Failed to delete schedule: {str(e)}"

    def load_data(self, file_type: str) -> Tuple[bool, List[Dict[str, Any]], str]:
        """Load data from specified file type"""
        try:
            if file_type == "employees":
                file_path = self.staff_file
                if not file_path.exists():
                    return True, [], ""
                with file_path.open('r', newline='', encoding='utf-8-sig') as f:
                    return True, list(csv.DictReader(f)), ""

            elif file_type == "schedules":
                if not self.schedules_file.exists():
                    return True, [], ""
                with self.schedules_file.open('r', newline='', encoding='utf-8-sig') as f:
                    return True, list(csv.DictReader(f)), ""

            elif file_type == "wage_rates":
                if not self.pay_rates_file.exists():
                    return True, [], ""
                with self.pay_rates_file.open('r') as f:
                    rates = json.load(f)
                    return True, [{"position": k, **v} for k, v in rates.items()], ""

            return False, [], f"Invalid file type: {file_type}"

        except Exception as e:
            return False, [], f"Error loading {file_type}: {str(e)}"

    def save_data(self, file_type: str, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Save data to specified file type"""
        try:
            if file_type == "employees":
                if not data:
                    return True, "No data to save"
                headers = ['staff_id', 'fname', 'lname', 'job', 'start']
                with self.staff_file.open('w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data)

            elif file_type == "schedules":
                if not data:
                    return True, "No data to save"
                headers = [
                    'schedule_id', 'employee_id', 'week_start',
                    'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
                    'total_hours', 'total_pay'
                ]
                with self.schedules_file.open('w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data)

            elif file_type == "wage_rates":
                rates_dict = {item['position']: {
                    'base_rate': item['base_rate'],
                    'weekend_rate': item['weekend_rate']
                } for item in data}
                with self.pay_rates_file.open('w') as f:
                    json.dump(rates_dict, f, indent=4)
            else:
                return False, f"Invalid file type: {file_type}"

            return True, f"{file_type} saved successfully"

        except Exception as e:
            return False, f"Error saving {file_type}: {str(e)}"

    def add_record(self, file_type: str, record: Dict[str, Any]) -> Tuple[bool, str]:
        """Add new record after checking for duplicate IDs"""
        try:
            # Get ID field name based on file type
            id_field = {
                "employees": "staff_id",
                "schedules": "schedule_id",
                "wage_rates": "position"
            }.get(file_type)

            if not id_field:
                return False, f"Invalid file type: {file_type}"

            # Check for duplicate ID
            if self.check_duplicate_id(file_type, record[id_field]):
                return False, f"Duplicate {id_field} found"

            # Validate record
            valid, msg = self.validate_record(file_type, record)
            if not valid:
                return False, msg

            # Load existing data
            success, data, error = self.load_data(file_type)
            if not success:
                return False, error

            # Add new record and save
            data.append(record)
            return self.save_data(file_type, data)

        except Exception as e:
            return False, f"Error adding record: {str(e)}"

    def update_record(self, file_type: str, record_id: str, **kwargs) -> Tuple[bool, str]:
        """Update existing record with new values"""
        try:
            success, data, error = self.load_data(file_type)
            if not success:
                return False, error

            id_field = {
                "employees": "staff_id",
                "schedules": "schedule_id",
                "wage_rates": "position"
            }.get(file_type)

            if not id_field:
                return False, f"Invalid file type: {file_type}"

            # Find and update record
            found = False
            for record in data:
                if record[id_field] == record_id:
                    record.update(kwargs)
                    found = True
                    break

            if not found:
                return False, f"Record with {id_field}={record_id} not found"

            return self.save_data(file_type, data)

        except Exception as e:
            return False, f"Error updating record: {str(e)}"

    def delete_record(self, file_type: str, record_id: str) -> Tuple[bool, str]:
        """Delete record by ID"""
        try:
            success, data, error = self.load_data(file_type)
            if not success:
                return False, error

            id_field = {
                "employees": "staff_id",
                "schedules": "schedule_id",
                "wage_rates": "position"
            }.get(file_type)

            if not id_field:
                return False, f"Invalid file type: {file_type}"

            # Filter out the record to delete
            original_length = len(data)
            data = [record for record in data if record[id_field] != record_id]

            if len(data) == original_length:
                return False, f"Record with {id_field}={record_id} not found"

            return self.save_data(file_type, data)

        except Exception as e:
            return False, f"Error deleting record: {str(e)}"

    def validate_record(self, file_type: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate record based on file type"""
        try:
            if file_type == "employees":
                required = ['staff_id', 'fname', 'lname', 'job', 'start']
                for field in required:
                    if field not in data:
                        return False, f"Missing required field: {field}"
                # Validate date format
                try:
                    datetime.strptime(data['start'], '%d-%m-%Y')
                except ValueError:
                    return False, "Invalid date format. Use DD-MM-YYYY"

            elif file_type == "schedules":
                required = ['schedule_id', 'employee_id', 'week_start',
                          'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                for field in required:
                    if field not in data:
                        return False, f"Missing required field: {field}"
                # Validate hours
                for day in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
                    try:
                        hours = float(data[day])
                        if hours < 0 or hours > 12:
                            return False, f"Invalid hours for {day}: must be between 0 and 12"
                    except ValueError:
                        return False, f"Invalid hours format for {day}"

            elif file_type == "wage_rates":
                required = ['position', 'base_rate', 'weekend_rate']
                for field in required:
                    if field not in data:
                        return False, f"Missing required field: {field}"
                # Validate rates
                try:
                    if float(data['base_rate']) <= 0 or float(data['weekend_rate']) <= 0:
                        return False, "Rates must be greater than zero"
                except ValueError:
                    return False, "Invalid rate format"

            return True, ""

        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def check_duplicate_id(self, file_type: str, new_id: str) -> bool:
        """Check if ID already exists in file"""
        success, data, _ = self.load_data(file_type)
        if not success or not data:
            return False

        id_field = {
            "employees": "staff_id",
            "schedules": "schedule_id",
            "wage_rates": "position"
        }.get(file_type)

        return any(record[id_field] == new_id for record in data)

