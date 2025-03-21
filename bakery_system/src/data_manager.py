from pathlib import Path
import json
import csv
from typing import Tuple, List, Dict, Any

class DataManager:
    def __init__(self, data_folder: str = "data"):
        self.data_folder = Path(data_folder)
        self.pay_rates_file = self.data_folder / "wage_rates.json"
        self.schedules_file = self.data_folder / "schedules.csv"

    def setup_data_folder(self) -> Tuple[bool, str]:
        try:
            self.data_folder.mkdir(exist_ok=True)
            
            if not self.pay_rates_file.exists():
                self._create_pay_rates()
            
            if not self.schedules_file.exists():
                self._create_schedules_file()
                
            return True, ""
        except Exception as e:
            return False, f"Couldn't set up data folder: {str(e)}"

    def _create_pay_rates(self):
        starter_rates = {
            "Baker": {"base": 16.00, "weekend": 19.00},
            "Counter Staff": {"base": 14.00, "weekend": 16.50}
        }
        with self.pay_rates_file.open('w') as f:
            json.dump(starter_rates, f, indent=4)

    def _create_schedules_file(self):
        headers = ['schedule_id', 'employee_id', 'week_start_date', 
                  'mon_hours', 'tue_hours', 'wed_hours', 'thu_hours', 
                  'fri_hours', 'sat_hours', 'sun_hours', 'total_hours', 'total_pay']
        
        with self.schedules_file.open('w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def save_schedule(self, schedule) -> Tuple[bool, str]:
        try:
            if not self.schedules_file.exists():
                self._create_schedules_file()

            row = [
                schedule.schedule_id,
                schedule.employee_id,
                schedule.week_start_date,
                schedule.hours['mon'],
                schedule.hours['tue'],
                schedule.hours['wed'],
                schedule.hours['thu'],
                schedule.hours['fri'],
                schedule.hours['sat'],
                schedule.hours['sun'],
                schedule.total_hours,
                schedule.total_pay
            ]

            with self.schedules_file.open('a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(row)

            return True, ""
        except Exception as e:
            return False, str(e)

    def load_schedules(self) -> Tuple[bool, List[Dict[str, Any]], str]:
        try:
            if not self.schedules_file.exists():
                return True, [], "No schedules file exists yet"

            schedules = []
            with self.schedules_file.open('r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                schedules = list(reader)
            
            return True, schedules, ""
        except Exception as e:
            return False, [], str(e)

    def delete_schedule(self, schedule_id: str) -> Tuple[bool, str]:
        try:
            success, schedules, error = self.load_schedules()
            if not success:
                return False, error

            updated_schedules = [s for s in schedules if s['schedule_id'] != schedule_id]
            
            if len(updated_schedules) == len(schedules):
                return False, "Schedule not found"

            with self.schedules_file.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=schedules[0].keys())
                writer.writeheader()
                writer.writerows(updated_schedules)

            return True, ""
        except Exception as e:
            return False, str(e)  # Add this line to handle exceptions

