import csv
from pathlib import Path
from datetime import datetime
from tabulate import tabulate

STAFF_FILE = Path("data/employees.csv")

def setup_staff_file():
    """Makes the employees CSV file if it doesn't exist"""
    if not STAFF_FILE.exists():
        STAFF_FILE.parent.mkdir(parents=True, exist_ok=True)
        with STAFF_FILE.open(mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['staff_id', 'fname', 'lname', 'job', 'start'])

def make_staff_id():
    """Generate a unique ID"""
    if not STAFF_FILE.exists():
        return "E001"
    
    try:
        with STAFF_FILE.open(mode='r', newline='', encoding='utf-8-sig') as file:
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

def add_staff(fname, lname, job, start_date):
    """Add new staff to the system"""
    if not fname or not lname or not job:
        raise ValueError("All fields need to be filled in!")
    
    try:
        datetime.strptime(start_date, '%d-%m-%Y')
    except ValueError:
        raise ValueError("Date should be DD-MM-YYYY format!")

    staff_id = make_staff_id()
    
    with STAFF_FILE.open(mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow([staff_id, fname, lname, job, start_date])

def find_staff(staff_id):
    """Find a staff member by their ID"""
    with STAFF_FILE.open(mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for person in reader:
            if person['staff_id'] == staff_id:
                return person
    return None

def update_staff_name(staff_id, new_fname, new_lname):
    """Update a staff member's name"""
    if not new_fname or not new_lname:
        raise ValueError("Names can't be empty!")
    
    staff_list = []
    found = False
    
    with STAFF_FILE.open(mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        headers = next(reader)
        staff_list.append(headers)
        for person in reader:
            if person and person[0] == staff_id:
                person[1] = new_fname
                person[2] = new_lname
                found = True
            staff_list.append(person)
    
    if found:
        with STAFF_FILE.open(mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerows(staff_list)
    else:
        raise ValueError("Couldn't find that staff member!")

def remove_staff(staff_id):
    """Remove a staff member from the system"""
    staff_list = []
    found = False
    
    with STAFF_FILE.open(mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        headers = next(reader)
        staff_list.append(headers)
        for person in reader:
            if person and person[0] != staff_id:
                staff_list.append(person)
            elif person and person[0] == staff_id:
                found = True
    
    if not found:
        raise ValueError("Couldn't find that staff member!")
    
    with STAFF_FILE.open(mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(staff_list)

def show_staff_list():
    """Display table of all staff members"""
    with STAFF_FILE.open(mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        all_staff = list(reader)
    
    print(tabulate(all_staff, headers="firstrow", tablefmt="grid"))
