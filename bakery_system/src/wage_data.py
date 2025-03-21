import json
from pathlib import Path
from typing import Dict, Optional

class WageManager:
    def __init__(self):
        self.wage_file = Path("data/wage_rates.json")
    
    def setup_wage_file(self) -> None:
        """Creates wage rates file if it doesn't exist"""
        default_wage_data = {
            "Head Baker": {"base": 18.50, "weekend": 22.00},
            "Baker": {"base": 16.00, "weekend": 19.00},
            "Pastry Chef": {"base": 16.50, "weekend": 19.50},
            "Counter Staff": {"base": 14.00, "weekend": 16.50},
            "Kitchen Assistant": {"base": 13.50, "weekend": 16.00}
        }

        if not self.wage_file.exists():
            self.wage_file.parent.mkdir(parents=True, exist_ok=True)
            with self.wage_file.open('w') as f:
                json.dump(default_wage_data, f, indent=4)

    def validate_rate(self, rate: float, rate_type: str) -> None:
        if rate <= 0:
            raise ValueError(f"Invalid {rate_type}: must be greater than zero")

    def add_job_rate(self, job_title: str, base_rate: float, weekend_rate: float) -> None:
        self.validate_rate(base_rate, "base rate")
        self.validate_rate(weekend_rate, "weekend rate")
        
        with self.wage_file.open(mode='r') as file:
            wage_data = json.load(file)
        
        if job_title in wage_data:
            raise ValueError(f"Job title '{job_title}' already exists")
        
        wage_data[job_title] = {'base': base_rate, 'weekend': weekend_rate}
        
        with self.wage_file.open(mode='w') as file:
            json.dump(wage_data, file, indent=4)

    def get_job_rate(self, job_title: str) -> Optional[Dict[str, float]]:
        """Get the pay rates for a specific job title"""
        with self.wage_file.open(mode='r') as file:
            wage_data = json.load(file)
        
        if job_title not in wage_data:
            return None
        
        rates = wage_data[job_title]
        return {
            'base': rates['base'],
            'weekend': rates['weekend']
        }

    def update_job_rate(self, job_title: str, new_base: float, new_weekend: float) -> None:
        self.validate_rate(new_base, "base rate")
        self.validate_rate(new_weekend, "weekend rate")
        
        with self.wage_file.open(mode='r') as file:
            wage_data = json.load(file)
        
        if job_title not in wage_data:
            raise ValueError(f"Job title '{job_title}' not found")
        
        wage_data[job_title] = {'base': new_base, 'weekend': new_weekend}
        
        with self.wage_file.open(mode='w') as file:
            json.dump(wage_data, file, indent=4)

    def remove_job_rate(self, job_title: str) -> None:
        with self.wage_file.open(mode='r') as file:
            wage_data = json.load(file)
        
        if job_title not in wage_data:
            raise ValueError(f"Job title '{job_title}' not found")
        
        del wage_data[job_title]
        
        with self.wage_file.open(mode='w') as file:
            json.dump(wage_data, file, indent=4)
