from typing import Dict, Optional, Tuple

class WageManager:
    def __init__(self):
        pass

    @staticmethod
    def validate_rate(rate: float, rate_type: str) -> Tuple[bool, str]:
        """Validate wage rate"""
        if rate <= 0:
            return False, f"Invalid {rate_type}: must be greater than zero"
        return True, ""

    def validate_position(self, position: str, available_positions: Dict[str, Dict[str, float]]) -> Tuple[bool, str]:
        """Validate if position exists in wage rates"""
        if not position:
            return False, "Position cannot be empty"

        for stored_title in available_positions.keys():
            if stored_title.lower() == position.lower():
                return True, ""

        return False, f"Position '{position}' not found"

    def get_rate(self, position: str, is_weekend: bool, rates: Dict[str, Dict[str, float]]) -> Tuple[bool, float, str]:
        """Get wage rate for a position"""
        for stored_title, rate_info in rates.items():
            if stored_title.lower() == position.lower():
                rate_key = 'weekend_rate' if is_weekend else 'base_rate'
                return True, rate_info[rate_key], ""
        return False, 0.0, f"Position '{position}' not found"

    def calculate_pay(self, position: str, hours: Dict[str, float], rates: Dict[str, Dict[str, float]]) -> Tuple[bool, float, str]:
        """Calculate pay based on position and hours worked"""
        # Validate position exists
        valid, msg = self.validate_position(position, rates)
        if not valid:
            return False, 0.0, msg

        # Get rates for this position
        position_rates = None
        for stored_title, rate_info in rates.items():
            if stored_title.lower() == position.lower():
                position_rates = rate_info
                break

        if not position_rates:
            return False, 0.0, f"No rates found for position '{position}'"

        # Calculate pay
        base_rate = position_rates['base_rate']
        weekend_rate = position_rates['weekend_rate']

        weekday_hours = sum([hours.get(day, 0) for day in ['mon', 'tue', 'wed', 'thu', 'fri']])
        weekend_hours = sum([hours.get(day, 0) for day in ['sat', 'sun']])

        total_pay = (weekday_hours * base_rate) + (weekend_hours * weekend_rate)
        return True, round(total_pay, 2), ""
