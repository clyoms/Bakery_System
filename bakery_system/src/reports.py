import os
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple
from data_manager import DataManager
from employee import Employee
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

    def generate_employee_schedule(self, employee_id: str, start_date: str, end_date: str) -> Tuple[bool, List[Dict[str, Any]], str]:
        try:
            success, schedules, message = self.data_manager.load_schedules_by_employee_id(employee_id)
            if not success:
                return False, [], message

            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            filtered = [
                sched for sched in schedules
                if start <= datetime.strptime(sched["week_start_date"], "%Y-%m-%d") <= end
            ]

            return True, filtered, "" if filtered else f"No schedules found for {employee_id} in the given range."
        except Exception as e:
            return False, [], f"Error generating schedule report: {str(e)}"

    def generate_wage_report(self, start_date: str, end_date: str) -> Tuple[bool, List[Dict[str, Any]], str]:
        try:
            success, schedules, message = self.data_manager.load_schedules()
            if not success:
                return False, [], message

            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            success, wage_data, error = self.wage_manager.get_all_rates()
            if not success:
                return False, [], error

            success, staff_list, error = self.employee_manager.get_all_staff()
            if not success:
                return False, [], error

            employee_map = {emp["staff_id"]: emp for emp in staff_list}
            report = []

            for sched in schedules:
                sched_date = datetime.strptime(sched["week_start_date"], "%Y-%m-%d")
                if not (start <= sched_date <= end):
                    continue

                emp_id = sched["employee_id"]
                emp = employee_map.get(emp_id)
                if not emp:
                    continue

                position = emp["job"]
                wage = wage_data.get(position, {"base": 0, "weekend": 0})
                base = wage["base"]
                weekend = wage["weekend"]

                total_hours = float(sched["total_hours"])
                total_pay = float(sched["total_pay"])

                report.append({
                    "staff_id": emp_id,
                    "name": f"{emp['fname']} {emp['lname']}",
                    "job": position,
                    "week_start_date": sched["week_start_date"],
                    "total_hours": total_hours,
                    "total_pay": round(total_pay, 2)
                })

            return True, report, ""
        except Exception as e:
            return False, [], f"Error generating wage report: {str(e)}"

    def save_csv_report(self, data: List[Dict[str, Any]], filename: str) -> Tuple[bool, str]:
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

    def save_text_report(self, data: List[Dict[str, Any]], filename: str, title: str) -> Tuple[bool, str]:
        try:
            from tabulate import tabulate
            if not data:
                return False, "No data to save"

            filepath = self.reports_folder / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with filepath.open('w', encoding='utf-8') as f:
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n\n")
                table = tabulate(data, headers="keys", tablefmt="grid")
                f.write(table)
            
            return True, f"Report saved to {filepath}"
        except Exception as e:
            return False, f"Failed to save report: {str(e)}"

