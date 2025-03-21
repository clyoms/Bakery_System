import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from .schedule import Schedule

class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.wage_rates_file = self.data_dir / "wage_rates.json"

    def initialize_data_directory(self) -> Tuple[bool, str]:
        try:
            self.data_dir.mkdir(exist_ok=True)
            
            if not self.wage_rates_file.exists():
                self._create_wage_rates_file()
                
            return True, ""
        except Exception as e:
            return False, f"Failed to initialize data directory: {str(e)}"

    def _create_wage_rates_file(self):
        default_rates = {
            "Baker": {"base_rate": 16.00, "weekend_rate": 19.00},
            "Counter Staff": {"base_rate": 14.00, "weekend_rate": 16.50}
        }
        with self.wage_rates_file.open('w') as f:
            json.dump(default_rates, f, indent=4)

    def load_wage_rates(self) -> Tuple[bool, Dict[str, Dict[str, float]], str]:
        try:
            with self.wage_rates_file.open('r') as f:
                wage_rates = json.load(f)
            return True, wage_rates, ""
        except Exception as e:
            return False, {}, f"Failed to load wage rates: {str(e)}"

    def save_wage_rates(self, wage_rates: Dict[str, Dict[str, float]]) -> Tuple[bool, str]:
        try:
            with self.wage_rates_file.open('w') as f:
                json.dump(wage_rates, f, indent=4)
            return True, ""
        except Exception as e:
            return False, f"Failed to save wage rates: {str(e)}"

    def get_position_rate(self, position: str) -> Tuple[bool, Optional[Dict[str, float]], str]:
        success, wage_rates, error = self.load_wage_rates()
        if not success:
            return False, None, error
        
        if position not in wage_rates:
            return False, None, f"Position '{position}' not found"
        
        return True, wage_rates[position], ""

    def update_position_rate(self, position: str, base_rate: float, weekend_rate: float) -> Tuple[bool, str]:
        success, wage_rates, error = self.load_wage_rates()
        if not success:
            return False, error
        
        if position not in wage_rates:
            return False, f"Position '{position}' not found"
        
        wage_rates[position] = {
            "base_rate": base_rate,
            "weekend_rate": weekend_rate
        }
        
        return self.save_wage_rates(wage_rates)

    def add_position_rate(self, position: str, base_rate: float, weekend_rate: float) -> Tuple[bool, str]:
        success, wage_rates, error = self.load_wage_rates()
        if not success:
            return False, error
        
        if position in wage_rates:
            return False, f"Position '{position}' already exists"
        
        wage_rates[position] = {
            "base_rate": base_rate,
            "weekend_rate": weekend_rate
        }
        
        return self.save_wage_rates(wage_rates)

    def delete_position_rate(self, position: str) -> Tuple[bool, str]:
        success, wage_rates, error = self.load_wage_rates()
        if not success:
            return False, error
        
        if position not in wage_rates:
            return False, f"Position '{position}' not found"
        
        del wage_rates[position]
        return self.save_wage_rates(wage_rates)

