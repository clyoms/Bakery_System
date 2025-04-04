import csv
from pathlib import Path
from typing import List, Dict, Tuple, Any
from datetime import datetime
from tabulate import tabulate

class Reports:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.reports_folder = Path("data/reports")
        self.setup_reports_folder()

    def setup_reports_folder(self) -> Tuple[bool, str]:
        """Create reports folder if it doesn't exist"""
        try:
            self.reports_folder.mkdir(parents=True, exist_ok=True)
            return True, ""
        except Exception as e:
            return False, f"Failed to create reports folder: {str(e)}"

    def generate_employee_report(self, sort_by: str = "name") -> Tuple[bool, List[Dict[str, Any]], str]:
        """
        Generate a comprehensive employee report sorted by specified field

        Args:
            sort_by (str): Field to sort by ("name" or "position")

        Returns:
            Tuple[bool, List[Dict[str, Any]], str]: (Success status, Report data, Error message)
        """
        try:
            # Get all employees
            success, employees, error = self.data_manager.get_all_employees()
            if not success:
                return False, [], error

            # Format employee data for report
            report_data = []
            for emp in employees:
                # Calculate tenure
                start_date = datetime.strptime(emp['start'], '%d-%m-%Y')
                tenure_days = (datetime.now() - start_date).days

                report_entry = {
                    'Employee ID': emp['staff_id'],
                    'First Name': emp['fname'],
                    'Last Name': emp['lname'],
                    'Position': emp['job'],
                    'Start Date': emp['start'],
                    'Tenure (days)': tenure_days
                }
                report_data.append(report_entry)

            # Sort the report data
            if sort_by.lower() == "name":
                report_data.sort(key=lambda x: f"{x['Last Name']}, {x['First Name']}".lower())
            else:  # sort by position
                report_data.sort(key=lambda x: x['Position'].lower())

            return True, report_data, ""
        except Exception as e:
            return False, [], f"Failed to generate employee report: {str(e)}"

    def generate_wage_report(self, start_date: str, end_date: str) -> Tuple[bool, List[Dict[str, Any]], str]:
        """
        Generate a comprehensive wage report for all employees within a date range

        Args:
            start_date (str): Start date in DD-MM-YYYY format
            end_date (str): End date in DD-MM-YYYY format

        Returns:
            Tuple[bool, List[Dict[str, Any]], str]: (Success status, Report data, Error message)
        """
        try:
            # Validate dates
            try:
                start = datetime.strptime(start_date, '%d-%m-%Y')
                end = datetime.strptime(end_date, '%d-%m-%Y')
                if start > end:
                    return False, [], "Start date must be before end date"
            except ValueError:
                return False, [], "Invalid date format. Use DD-MM-YYYY"

            # Get all schedules within date range
            success, schedules, error = self.data_manager.get_schedules(
                start_date=start_date,
                end_date=end_date
            )

            if not success:
                return False, [], error

            # Get wage rates
            success, wage_rates, error = self.data_manager.get_wage_rates()
            if not success:
                return False, [], error

            # Group schedules by employee
            employee_wages = {}
            for schedule in schedules:
                emp_id = schedule['employee_id']
                if emp_id not in employee_wages:
                    # Get employee details
                    success, employee, error = self.data_manager.get_employee(emp_id)
                    if not success:
                        continue

                    # Get wage rates for position
                    position = employee['job']
                    base_rate = 0.0
                    weekend_rate = 0.0

                    # Find the rate for this position
                    for pos, rates in wage_rates.items():
                        if pos.lower() == position.lower():
                            base_rate = rates['base_rate']
                            weekend_rate = rates['weekend_rate']
                            break

                    employee_wages[emp_id] = {
                        'Employee ID': emp_id,
                        'Name': f"{employee['fname']} {employee['lname']}",
                        'Position': position,
                        'Base Rate': base_rate,
                        'Weekend Rate': weekend_rate,
                        'Regular Hours': 0.0,
                        'Weekend Hours': 0.0,
                        'Total Hours': 0.0,
                        'Regular Pay': 0.0,
                        'Weekend Pay': 0.0,
                        'Total Pay': 0.0
                    }

                # Calculate regular and weekend hours
                regular_hours = sum(float(schedule[day]) for day in ['mon', 'tue', 'wed', 'thu', 'fri'])
                weekend_hours = sum(float(schedule[day]) for day in ['sat', 'sun'])

                emp_data = employee_wages[emp_id]
                emp_data['Regular Hours'] += regular_hours
                emp_data['Weekend Hours'] += weekend_hours
                emp_data['Total Hours'] += regular_hours + weekend_hours
                emp_data['Regular Pay'] += regular_hours * emp_data['Base Rate']
                emp_data['Weekend Pay'] += weekend_hours * emp_data['Weekend Rate']
                emp_data['Total Pay'] += float(schedule['total_pay'])

            return True, list(employee_wages.values()), ""
        except Exception as e:
            return False, [], f"Failed to generate wage report: {str(e)}"

    def export_to_csv(self, data: List[Dict[str, Any]], filename: str) -> Tuple[bool, str]:
        try:
            if not data:
                return False, "No data to export"

            # Generate timestamped filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = self.reports_folder / f"{filename}_{timestamp}.csv"

            # Write data to CSV
            with file_path.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            return True, str(file_path)
        except Exception as e:
            return False, f"Failed to export to CSV: {str(e)}"

    def export_to_txt(self, data: List[Dict[str, Any]], filename: str) -> Tuple[bool, str]:
        try:
            if not data:
                return False, "No data to export"

            # Generate timestamped filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = self.reports_folder / f"{filename}_{timestamp}.txt"

            # Format data using tabulate
            headers = data[0].keys()
            rows = [row.values() for row in data]
            table = tabulate(rows, headers=headers, tablefmt="grid")

            # Add report header and timestamp
            report_text = (
                f"Report: {filename}\n"
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"{table}\n"
            )

            # Write to file
            with file_path.open('w', encoding='utf-8') as f:
                f.write(report_text)

            return True, str(file_path)
        except Exception as e:
            return False, f"Failed to export to TXT: {str(e)}"

    def create_staff_list(self, sort_by: str = "lname") -> Tuple[bool, List[Dict[str, Any]], str]:
        """Generate a sorted list of all employees"""
        try:
            # Get all employees
            success, employees, error = self.data_manager.get_all_employees()
            if not success:
                return False, [], error

            # Sort employees
            if sort_by == "lname":
                employees.sort(key=lambda x: x['lname'].lower())
            else:  # sort by job
                employees.sort(key=lambda x: x['job'].lower())

            return True, employees, ""
        except Exception as e:
            return False, [], f"Failed to create staff list: {str(e)}"

    def save_csv_report(self, data: List[Dict[str, Any]], filename: str) -> Tuple[bool, str]:
        """Save report to CSV file"""
        return self.export_to_csv(data, filename)

    def save_text_report(self, data: List[Dict[str, Any]], filename: str) -> Tuple[bool, str]:
        """Save report to text file"""
        return self.export_to_txt(data, filename)

    def generate_employee_schedule(self, employee_id: str, start_date: str, end_date: str) -> Tuple[bool, List[Dict[str, Any]], str]:
        """Generate schedule report for an employee"""
        try:
            # Validate dates
            try:
                if start_date:
                    try:
                        datetime.strptime(start_date, '%d-%m-%Y')
                    except ValueError:
                        # Try alternative format
                        datetime.strptime(start_date, '%Y-%m-%d')
                if end_date:
                    try:
                        datetime.strptime(end_date, '%d-%m-%Y')
                    except ValueError:
                        # Try alternative format
                        datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return False, [], "Invalid date format. Use DD-MM-YYYY or YYYY-MM-DD"

            # Get employee
            success, employee, error = self.data_manager.get_employee(employee_id)
            if not success:
                return False, [], f"Employee not found: {error}"

            # Get schedules
            success, schedules, error = self.data_manager.get_schedules(
                employee_id=employee_id,
                start_date=start_date,
                end_date=end_date
            )
            if not success:
                return False, [], error

            if not schedules:
                return False, [], "No schedules found for this employee in the specified date range"

            # Format schedules for report
            for schedule in schedules:
                schedule['Employee Name'] = f"{employee['fname']} {employee['lname']}"
                schedule['Position'] = employee['job']

            return True, schedules, ""
        except Exception as e:
            return False, [], f"Failed to generate employee schedule: {str(e)}"

