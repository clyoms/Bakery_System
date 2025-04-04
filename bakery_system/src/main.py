from data_manager import DataManager
from reports import Reports
from schedule import Schedule
from tabulate import tabulate
from datetime import datetime

# Initialize managers
data_manager = DataManager()
reports = Reports(data_manager)

def display_main_menu():
    print("Welcome to Murphy's Bakery Management System:")
    print("1. Employee Management")
    print("2. Schedule Management")
    print("3. Wages and Positions")
    print("4. Reports")
    print("5. Exit")

def employee_management():
    while True:
        print("\n----- Employee Management -----")
        print("1. Add New Employee")
        print("2. View Employee Details")
        print("3. Update Employee Record")
        print("4. Delete Employee")
        print("5. List All Employees")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == '0':
            break
        elif choice == '1':
            fname = input("First name: ").strip()
            lname = input("Last name: ").strip()
            job = input("Job title: ").strip()
            start_date = input("Start date (DD-MM-YYYY): ").strip()

            success, msg = data_manager.add_employee(fname, lname, job, start_date)
            print(msg if success else f"Error: {msg}")

        elif choice == '2':
            emp_id = input("Enter Employee ID (e.g., E001): ").strip()
            if not emp_id.startswith('E') or not emp_id[1:].isdigit():
                print("Error: Invalid ID format. Use E followed by numbers (e.g., E001)")
                continue

            success, employee, error = data_manager.get_employee(emp_id)
            if success and employee:
                print("\nEmployee Details:")
                print(tabulate([employee], headers="keys"))
            else:
                print(f"Employee not found: {error}")

        elif choice == '3':
            emp_id = input("Employee ID: ").strip()
            new_fname = input("New first name (or press Enter to skip): ").strip()
            new_lname = input("New last name (or press Enter to skip): ").strip()
            new_job = input("New job title (or press Enter to skip): ").strip()

            # Skip empty inputs
            new_fname = new_fname if new_fname else None
            new_lname = new_lname if new_lname else None
            new_job = new_job if new_job else None

            success, msg = data_manager.update_employee(emp_id, new_fname, new_lname, new_job)
            print("Updated successfully!" if success else f"Error: {msg}")

        elif choice == '4':
            emp_id = input("Employee ID to remove: ").strip()
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                success, msg = data_manager.delete_employee(emp_id)
                print("Employee removed successfully!" if success else f"Error: {msg}")

        elif choice == '5':
            success, staff_list, error = data_manager.get_all_employees()
            if success:
                print("\nAll Employees:")
                print(tabulate(staff_list, headers="keys"))
            else:
                print(f"Error: {error}")
        else:
            print("Invalid choice. Please try again.")

def schedule_management():
    while True:
        print("\n----- Schedule Management -----")
        print("1. Create/Update Weekly Schedule")
        print("2. View Schedule for Employee")
        print("3. Delete Schedule")
        print("4. List All Schedules")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == '0':
            break
        elif choice == '1':
            emp_id = input("Employee ID: ").strip()
            week_start = input("Week start date (DD-MM-YYYY): ").strip()

            # Create schedule ID using timestamp
            schedule_id = f"SCH_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            schedule = Schedule(schedule_id, emp_id, week_start, {})

            days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            daily_hours = {}

            for day in days:
                while True:
                    try:
                        hours = float(input(f"{day.capitalize()} hours: "))
                        if 0 <= hours <= 12:
                            daily_hours[day] = hours
                            break
                        print("Hours must be between 0 and 12")
                    except ValueError:
                        print("Please enter a valid number")

            # Validate total weekly hours
            if sum(daily_hours.values()) > 48:
                print("Error: Total weekly hours cannot exceed 48")
                continue

            schedule.hours = daily_hours
            success, msg = data_manager.save_schedule(schedule.__dict__)
            print(msg if success else f"Error: {msg}")

        elif choice == '2':
            emp_id = input("Employee ID: ").strip()
            start_date = input("Start date (DD-MM-YYYY): ").strip()
            end_date = input("End date (DD-MM-YYYY): ").strip()

            success, schedules, error = reports.generate_employee_schedule(emp_id, start_date, end_date)
            if success:
                print("\nEmployee Schedule:")
                print(tabulate(schedules, headers="keys"))
            else:
                print(f"Error: {error}")

        elif choice == '3':
            schedule_id = input("Schedule ID: ").strip()
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                success, msg = data_manager.delete_schedule(schedule_id)
                print("Schedule deleted!" if success else f"Error: {msg}")

        elif choice == '4':
            success, schedules, error = data_manager.get_schedules()
            if success:
                print("\nAll Schedules:")
                print(tabulate(schedules, headers="keys"))
            else:
                print(f"Error: {error}")
        else:
            print("Invalid choice. Please try again.")

def wage_calculations():
    while True:
        print("\n----- Wages and Positions -----")
        print("1. Calculate Weekly Wage for Employee")
        print("2. View Position Wage Rates")
        print("3. Update Position Rates")
        print("4. Add New Position")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == '0':
            break
        elif choice == '1':
            emp_id = input("Employee ID: ").strip()
            start_date = input("Week start date (DD-MM-YYYY): ").strip()

            success, schedule_report, error = reports.generate_employee_schedule(
                emp_id, start_date, start_date
            )

            if success and schedule_report:
                print("\nWage Calculation:")
                print(tabulate(schedule_report, headers="keys"))
            else:
                print(f"Error: {error}")

        elif choice == '2':
            success, rates, error = data_manager.get_wage_rates()
            if success:
                print("\nPosition Wage Rates:")
                formatted_rates = [
                    {"Position": pos, "Base Rate": rate["base_rate"], "Weekend Rate": rate["weekend_rate"]}
                    for pos, rate in rates.items()
                ]
                print(tabulate(formatted_rates, headers="keys"))
            else:
                print(f"Error retrieving wage rates: {error}")

        elif choice == '3':
            # Update position rates
            # First show current rates
            success, rates, error = data_manager.get_wage_rates()
            if not success:
                print(f"Error retrieving wage rates: {error}")
                continue

            print("\nCurrent Position Wage Rates:")
            formatted_rates = [
                {"Position": pos, "Base Rate": rate["base_rate"], "Weekend Rate": rate["weekend_rate"]}
                for pos, rate in rates.items()
            ]
            print(tabulate(formatted_rates, headers="keys"))

            # Get position to update
            position = input("\nEnter position to update: ").strip()

            # Check if position exists
            position_exists = False
            for pos in rates.keys():
                if pos.lower() == position.lower():
                    position = pos  # Use the exact case from the file
                    position_exists = True
                    break

            if not position_exists:
                print(f"Error: Position '{position}' not found")
                continue

            # Get new rates
            try:
                base_rate = float(input(f"New base rate for {position} (current: {rates[position]['base_rate']}): ").strip())
                weekend_rate = float(input(f"New weekend rate for {position} (current: {rates[position]['weekend_rate']}): ").strip())

                # Update the rates
                success, msg = data_manager.update_wage_rate(position, base_rate, weekend_rate)
                print(msg if success else f"Error: {msg}")
            except ValueError:
                print("Error: Rates must be valid numbers")

        elif choice == '4':
            # Add new position
            position = input("Enter new position name: ").strip()

            # Check if position already exists
            success, rates, error = data_manager.get_wage_rates()
            if not success:
                print(f"Error retrieving wage rates: {error}")
                continue

            position_exists = False
            for pos in rates.keys():
                if pos.lower() == position.lower():
                    position_exists = True
                    break

            if position_exists:
                print(f"Error: Position '{position}' already exists")
                continue

            # Get rates for new position
            try:
                base_rate = float(input(f"Base rate for {position}: ").strip())
                weekend_rate = float(input(f"Weekend rate for {position}: ").strip())

                # Add the new position
                success, msg = data_manager.add_wage_rate(position, base_rate, weekend_rate)
                print(msg if success else f"Error: {msg}")
            except ValueError:
                print("Error: Rates must be valid numbers")
        else:
            print("Invalid choice. Please try again.")

def reports_menu():
    while True:
        print("\n----- Reports -----")
        print("1. Generate Employee List (Sorted by Name/Position)")
        print("2. Generate Wage Report for Period")
        print("3. Export Employee Report to CSV")
        print("4. Export Wage Report to TXT")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == '0':
            break
        elif choice == '1':
            sort_by = input("Sort by (name/position): ").strip().lower()
            field = "lname" if sort_by == "name" else "job"

            success, staff_report, error = reports.create_staff_list(sort_by=field)
            if success:
                print("\nEmployee List:")
                print(tabulate(staff_report, headers="keys"))
            else:
                print(f"Error: {error}")

        elif choice in ['2', '3', '4']:
            start_date = input("Start date (DD-MM-YYYY): ").strip()
            end_date = input("End date (DD-MM-YYYY): ").strip()

            success, wage_report, error = reports.generate_wage_report(start_date, end_date)
            if not success:
                print(f"Error: {error}")
                continue

            if choice == '2':
                print("\nWage Report:")
                print(tabulate(wage_report, headers="keys"))
            elif choice == '3':
                success, msg = reports.save_csv_report(wage_report, "wage_report")
                print("Report saved successfully!" if success else f"Error: {msg}")
            else:  # choice == '4'
                success, msg = reports.save_text_report(wage_report, "wage_report")
                print("Report saved successfully!" if success else f"Error: {msg}")
        else:
            print("Invalid choice. Please try again.")

def main():
    # Initialize all required files and folders
    data_manager.setup_data_folder()
    reports.setup_reports_folder()

    while True:
        display_main_menu()
        choice = input("\nChoose an option (1-5): ").strip()

        if choice == '1':
            employee_management()
        elif choice == '2':
            schedule_management()
        elif choice == '3':
            wage_calculations()
        elif choice == '4':
            reports_menu()
        elif choice == '5':
            print("\nThanks for using Murphy's Bakery Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
