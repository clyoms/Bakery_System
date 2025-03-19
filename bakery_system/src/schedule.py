from typing import Dict, Tuple, Any
from datetime import datetime

class Schedule:
    """
    Class representing a work schedule for an employee at Murphy's Bakery.
    Handles schedule data operations, hours calculation, and wage computation.
    """
    def __init__(self, schedule_id: str, employee_id: str, week_start_date: str,
                 mon_hours: float = 0, tue_hours: float = 0, wed_hours: float = 0,
                 thu_hours: float = 0, fri_hours: float = 0, sat_hours: float = 0,
                 sun_hours: float = 0):
        """
        Initialize a Schedule object with the provided attributes.
        """
        self.schedule_id = schedule_id
        self.employee_id = employee_id
        self.week_start_date = week_start_date
        self.hours = {
            'mon': mon_hours, 'tue': tue_hours,
            'wed': wed_hours, 'thu': thu_hours,
            'fri': fri_hours, 'sat': sat_hours,
            'sun': sun_hours
        }
        self.total_hours = self.calculate_total_hours()
        self.total_pay = 0.0

    @classmethod
    def from_dict(cls, schedule_data: Dict[str, Any]) -> 'Schedule':
        """
        Create a Schedule object from a dictionary.
        """
        return cls(
            schedule_id=schedule_data['schedule_id'],
            employee_id=schedule_data['employee_id'],
            week_start_date=schedule_data['week_start_date'],
            mon_hours=float(schedule_data['mon_hours']),
            tue_hours=float(schedule_data['tue_hours']),
            wed_hours=float(schedule_data['wed_hours']),
            thu_hours=float(schedule_data['thu_hours']),
            fri_hours=float(schedule_data['fri_hours']),
            sat_hours=float(schedule_data['sat_hours']),
            sun_hours=float(schedule_data['sun_hours'])
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Schedule object to a dictionary.
        """
        return {
            'schedule_id': self.schedule_id,
            'employee_id': self.employee_id,
            'week_start_date': self.week_start_date,
            'mon_hours': str(self.hours['mon']),
            'tue_hours': str(self.hours['tue']),
            'wed_hours': str(self.hours['wed']),
            'thu_hours': str(self.hours['thu']),
            'fri_hours': str(self.hours['fri']),
            'sat_hours': str(self.hours['sat']),
            'sun_hours': str(self.hours['sun']),
            'total_hours': str(self.total_hours),
            'total_pay': str(self.total_pay)
        }

    def validate(self) -> Tuple[bool, str]:
        """
        Validate schedule data according to business rules.
        """
        try:
            datetime.strptime(self.week_start_date, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
        
        for day, hours in self.hours.items():
            if hours < 0:
                return False, f"Hours for {day} cannot be negative"
            if hours > 12:
                return False, f"Hours for {day} cannot exceed 12"
        
        if self.total_hours > 40:
            return False, "Total weekly hours cannot exceed 40"
        
        return True, ""

    def calculate_total_hours(self) -> float:
        """
        Calculate the total hours worked in the week.
        """
        return sum(self.hours.values())

    def calculate_pay(self, position_rates: Dict[str, Dict[str, float]], position: str) -> Tuple[bool, float, str]:
        """
        Calculate total pay for the week based on hours worked and position rates.
        """
        if position not in position_rates:
            return False, 0.0, f"No wage rates found for position: {position}"
        
        rates = position_rates[position]
        base_rate = rates['base_rate']
        weekend_rate = rates['weekend_rate']
        
        weekday_hours = sum([self.hours[day] for day in ['mon', 'tue', 'wed', 'thu', 'fri']])
        weekend_hours = sum([self.hours[day] for day in ['sat', 'sun']])
        
        total_pay = (weekday_hours * base_rate) + (weekend_hours * weekend_rate)
        self.total_pay = round(total_pay, 2)
        
        return True, self.total_pay, ""

    def update_hours(self, day: str, hours: float) -> Tuple[bool, str]:
        """
        Update hours worked for a specific day.
        """
        if day not in self.hours:
            return False, f"Invalid day: {day}"
        
        if not (0 <= hours <= 12):
            return False, "Hours must be between 0 and 12"
        
        old_hours = self.hours[day]
        self.hours[day] = hours
        self.total_hours = self.calculate_total_hours()
        
        if self.total_hours > 40:
            self.hours[day] = old_hours
            self.total_hours = self.calculate_total_hours()
            return False, "Total weekly hours cannot exceed 40"

        return True, ""
