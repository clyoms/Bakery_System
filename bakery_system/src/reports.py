from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
import csv
from .data_manager import DataManager

class Reports:
    def __init__(self, data_manager: DataManager, reports_dir: str = "reports"):
        self.data_manager = data_manager
        self.reports_dir = Path(reports_dir)

    def initialize_reports_directory(self) -> Tuple[bool, str]:
        try:
            self.reports_dir.mkdir(exist_ok=True)
            return True, ""
        except Exception as e:
            return False, str(e)

    def generate_employee_list(self, sort_by: str = "last_name") -> Tuple[bool, List[Dict[str, str]], str]:
        success, employees, error = self.data_manager.load_employees()
        if not success:
            return False, [], error

        try:
            sorted_employees = sorted(employees, key=lambda x: x[sort_by])
            return True, sorted_employees, ""
        except Exception as e:
            return False, [], str(e)

    def generate_employee_schedule(self, employee_id: str, start_date: str, end_date: str) -> Tuple[bool, List[Dict[str, Any]], str]:
       
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            success, schedules, error = self.data_manager.load_schedules()
            if not success:
                return False, [], error

            filtered_schedules = [
                schedule for schedule in schedules
                if (schedule['employee_id'] == employee_id and
                    start <= datetime.strptime(schedule['week_start_date'], '%Y-%m-%d') <= end)
            ]
            
            return True, filtered_schedules, ""
        except Exception as e:
            return False, [], str(e)

    def generate_wage_report(self, start_date: str, end_date: str) -> Tuple[bool, List[Dict[str, Any]], str]:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            success, schedules, error = self.data_manager.load_schedules()
            if not success:
                return False, [], error

            wage_report = []
            for schedule in schedules:
                schedule_date = datetime.strptime(schedule['week_start_date'], '%Y-%m-%d')
                if start <= schedule_date <= end:
                    wage_report.append({
                        'employee_id': schedule['employee_id'],
                        'week_start_date': schedule['week_start_date'],
                        'total_hours': schedule['total_hours'],
                        'total_pay': schedule['total_pay']
                    })
            
            return True, wage_report, ""
        except Exception as e:
            return False, [], str(e)

    def export_report_to_csv(self, report_data: List[Dict[str, Any]], filename: str) -> Tuple[bool, str]:
        try:
            if not report_data:
                return False, "No data to export"

            filepath = self.reports_dir / f"{filename}.csv"
            with filepath.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=report_data[0].keys())
                writer.writeheader()
                writer.writerows(report_data)
            return True, ""
        except Exception as e:
            return False, str(e)

    def export_report_to_text(self, report_data: List[Dict[str, Any]], filename: str, title: str) -> Tuple[bool, str]:
        try:
            if not report_data:
                return False, "No data to export"

            filepath = self.reports_dir / f"{filename}.txt"
            with filepath.open('w', encoding='utf-8-sig') as f:
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n\n")
                
                headers = report_data[0].keys()
                header_row = " | ".join(headers)
                f.write(header_row + "\n")
                f.write("-" * len(header_row) + "\n")
                
                for row in report_data:
                    f.write(" | ".join(str(value) for value in row.values()) + "\n")
                    
            return True, ""
        except Exception as e:

