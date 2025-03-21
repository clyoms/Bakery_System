from pathlib import Path
from datetime import datetime
import csv
from typing import Tuple, List, Dict, Optional
from tabulate import tabulate

class Employee:
    def __init__(self, staff_id: Optional[str], fname: str, lname: str, job: str, start_date: str):
        self.staff_id = staff_id
        self.fname = fname
        self.lname = lname
        self.job = job
        self.start_date = start_date
        self.staff_file = Path("data/employees.csv")

    def setup_staff_file(self) -> None:
        """Creates the employees CSV file if it doesn't exist"""
        if not self.staff_file.exists():
            self.staff_file.parent.mkdir(parents=True, exist_ok=True)
            with self.staff_file.open(mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(['staff_id', 'fname', 'lname', 'job', 'start'])

    def make_staff_id(self) -> str:
        """Generate a unique staff ID"""
        if not self.staff_file.exists():
            return "E001"
        
        try:
            with self.staff_file.open(mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                next(reader)  # skip header
                staff_ids = [row[0] for row in reader if row]
            
            if not staff_ids:
                return "E001"
            
            last_num = int(staff_ids[-1][1:])
            return f"E{last_num + 1:03d}"
        except Exception as e:
            print(f"Problem making ID: {e}")
            return "E001"

    def add_new(self) -> Tuple[bool, str]:
        """Add a new employee to the system"""
        try:
            if not self.fname or not self.lname or not self.job:
                return False, "All fields must be filled in"

            try:
                datetime.strptime(self.start_date, '%d-%m-%Y')
            except ValueError:
                return False, "Invalid date format. Use DD-MM-YYYY"

            self.staff_id = self.make_staff_id()

            with self.staff_file.open('a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    self.staff_id,
                    self.fname,
                    self.lname,
                    self.job,
                    self.start_date
                ])
            return True, f"Employee added successfully with ID: {self.staff_id}"
        except Exception as e:
            return False, f"Error adding employee: {str(e)}"

    def get_all_staff(self) -> Tuple[bool, List[Dict[str, str]], str]:
        """Get all staff members"""
        try:
            if not self.staff_file.exists():
                return False, [], "No staff file exists"

            with self.staff_file.open('r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                staff_list = list(reader)
            return True, staff_list, ""
        except Exception as e:
            return False, [], str(e)

    def update(self) -> Tuple[bool, str]:
        """Update employee name"""
        try:
            success, staff_list, error = self.get_all_staff()
            if not success:
                return False, error

            updated = False
            updated_staff = []
            
            for staff in staff_list:
                if staff['staff_id'] == self.staff_id:
                    staff['fname'] = self.fname
                    staff['lname'] = self.lname
                    updated = True
                updated_staff.append(staff)

            if not updated:
                return False, "Staff member not found"

            with self.staff_file.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['staff_id', 'fname', 'lname', 'job', 'start'])
                writer.writeheader()
                writer.writerows(updated_staff)

            return True, ""
        except Exception as e:
            return False, str(e)

    def remove(self) -> Tuple[bool, str]:
        """Remove employee from system"""
        try:
            success, staff_list, error = self.get_all_staff()
            if not success:
                return False, error

            updated_staff = [s for s in staff_list if s['staff_id'] != self.staff_id]
            
            if len(updated_staff) == len(staff_list):
                return False, "Staff member not found"

            with self.staff_file.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['staff_id', 'fname', 'lname', 'job', 'start'])
                writer.writeheader()
                writer.writerows(updated_staff)

            return True, ""
        except Exception as e:
            return False, str(e)

    def show_staff_list(self) -> None:
        """Display a formatted table of all staff members"""
        success, staff_list, error = self.get_all_staff()
        if not success:
            print(f"Error: {error}")
            return

        if not staff_list:
            print("No staff members found.")
            return

        headers = ['Staff ID', 'First Name', 'Last Name', 'Job Title', 'Start Date']
        rows = [[person['staff_id'], person['fname'], person['lname'], 
                person['job'], person['start']] for person in staff_list]
        
        print("\nStaff List:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))


