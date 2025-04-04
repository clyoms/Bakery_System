from datetime import datetime
from typing import Dict, List, Tuple, Any

class Schedule:
    def __init__(self, schedule_id: str, employee_id: str, week_start_date: str, daily_hours: Dict[str, float]):
        self.schedule_id = schedule_id
        self.employee_id = employee_id
        self.week_start_date = week_start_date
        self.hours = daily_hours
        self.total_hours = 0.0
        self.total_pay = 0.0

    @classmethod
    def validate_hours(cls, daily_hours: Dict[str, float]) -> Tuple[bool, str]:
        """Validates daily and weekly hours against legal limits"""
        try:
            # Check daily limits (≤12h)
            for day, hours in daily_hours.items():
                if hours < 0 or hours > 12:
                    return False, f"Invalid hours for {day}: must be between 0 and 12"

            # Check weekly limit (≤48h)
            total_weekly = sum(daily_hours.values())
            if total_weekly > 48:
                return False, "Weekly hours cannot exceed 48"

            return True, ""
        except Exception as e:
            return False, f"Error validating hours: {str(e)}"

    def validate(self) -> Tuple[bool, str]:
        """Validate all schedule data"""
        # Check if employee ID is provided
        if not self.employee_id:
            return False, "Employee ID is required"

        # Check if week start date is valid
        try:
            datetime.strptime(self.week_start_date, '%d-%m-%Y')
        except ValueError:
            return False, "Invalid date format. Use DD-MM-YYYY"

        # Validate hours
        return self.validate_hours(self.hours)

    def calculate_total_hours(self) -> float:
        """Calculate total hours worked in the week"""
        self.total_hours = sum(self.hours.values())
        return self.total_hours

    def to_dict(self) -> Dict[str, Any]:
        """Convert schedule to dictionary for storage"""
        return {
            'schedule_id': self.schedule_id,
            'employee_id': self.employee_id,
            'week_start': self.week_start_date,
            'mon': self.hours.get('mon', 0),
            'tue': self.hours.get('tue', 0),
            'wed': self.hours.get('wed', 0),
            'thu': self.hours.get('thu', 0),
            'fri': self.hours.get('fri', 0),
            'sat': self.hours.get('sat', 0),
            'sun': self.hours.get('sun', 0),
            'total_hours': self.total_hours,
            'total_pay': self.total_pay
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Schedule':
        """Create Schedule object from dictionary data"""
        daily_hours = {
            'mon': float(data.get('mon', 0)),
            'tue': float(data.get('tue', 0)),
            'wed': float(data.get('wed', 0)),
            'thu': float(data.get('thu', 0)),
            'fri': float(data.get('fri', 0)),
            'sat': float(data.get('sat', 0)),
            'sun': float(data.get('sun', 0))
        }

        schedule = cls(
            data.get('schedule_id'),
            data.get('employee_id'),
            data.get('week_start'),
            daily_hours
        )
        schedule.total_hours = float(data.get('total_hours', 0))
        schedule.total_pay = float(data.get('total_pay', 0))
        return schedule

    @staticmethod
    def generate_schedule_id(existing_ids: List[str]) -> str:
        """Generate a unique schedule ID"""
        if not existing_ids:
            return "S001"

        # Find the highest ID number
        highest_num = 0
        for schedule_id in existing_ids:
            if schedule_id.startswith('S'):
                try:
                    id_num = int(schedule_id[1:])
                    highest_num = max(highest_num, id_num)
                except ValueError:
                    # Skip IDs that don't follow the expected format
                    continue

        return f"S{highest_num + 1:03d}"
