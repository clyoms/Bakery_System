from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
import csv
from employee import Employee
from data_manager import DataManager
from wage_data import WageManager

class Reports:
    def __init__(self, employee_manager: Employee, data_manager: DataManager, wage_manager: WageManager):
        self.employee_manager = employee_manager
        self.data_manager = data_manager
        self.wage_manager = wage_manager
        self.reports_folder = Path("reports")

    def setup_reports_folder(self) -> None:
        """Creates reports folder if it doesn't exist"""
        self.reports_folder.mkdir(exist_ok=True)

    def create_staff_list(self, sort_by: str = "lname") -> Tuple[bool, List[Dict[str, str]], str]:
        """Generate sorted list of all staff members"""
        success, staff_list, error = self.employee_manager.get_all_staff()
        if not success:
            return False, [], error

        try:
            sorted_staff = sorted(staff_list, key=lambda x: x[sort_by].lower())
            return True, sorted_staff, ""
        except Exception as e:
            return False, [], f"Failed to sort staff list: {str(e)}"

    def save_csv_report(self, data: List[Dict[str, Any]], filename: str) -> Tuple[bool, str]:
        """Save report data to CSV file"""
        try:
            if not data:
                return False, "No data to save"

            filepath = self.reports_folder / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with filepath.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            
            return True, f"Report saved to {filepath}"
        except Exception as e:
            return False, f"Failed to save report: {str(e)}"

