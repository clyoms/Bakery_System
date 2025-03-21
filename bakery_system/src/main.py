import os
import csv
from pathlib import Path
from employee import Employee
from wage_data import WageManager
from reports import Reports
from data_manager import DataManager
from tabulate import tabulate


# Keep data organized in one place
DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

# Initialize managers
employee_manager = Employee(None, "", "", "", "")  
wage_manager = WageManager()
data_manager = DataManager()
reports = Reports(employee_manager, data_manager, wage_manager)  

# Get everything ready
employee_manager.setup_staff_file()
wage_manager.setup_wage_file()
reports.setup_reports_folder()

def show_menu():
    print("\nBakery Staff Management")
    print("----------------------")
    print("1. Add New Staff Member")
    print("2. Look Up Staff Member")
    print("3. Update Staff Name")
    print("4. Remove Staff Member")
    print("5. Add New Job Pay Rate")
    print("6. Check Job Pay Rate")
    print("7. Update Job Pay Rate")
    print("8. Remove Job Pay Rate")
    print("9. Show All Staff")
    print("10. Generate Staff List Report")
    print("11. Generate Employee Schedule Report")
    print("12. Generate Wage Report (CSV)")
    print("13. Generate Wage Report (Text)")
    print("14. Exit System")

def run_system():
    while True:
        try:
            show_menu()
            choice = input("\nWhat would you like to do? ").strip()

            if choice == '1':
                fname = input("First name: ").strip()
                lname = input("Last name: ").strip()
                job = input("Job title: ").strip()
                start = input("Start date (DD-MM-YYYY): ").strip()
                
                # Create a new employee instance
                new_employee = Employee(None, fname, lname, job, start)
                new_employee.setup_staff_file()  # Ensure the file exists
                success, message = new_employee.add_new()
                
                if success:
                    print(f"Great! {message}")
                else:
                    print(f"Something went wrong: {message}")

            elif choice == '2':
                staff_id = input("Staff ID number: ").strip()
                temp_employee = Employee(staff_id, "", "", "", "")
                success, staff_list, error = temp_employee.get_all_staff()
                if success:
                    staff = next((s for s in staff_list if s['staff_id'] == staff_id), None)
                    if staff:
                        print("\nStaff Details:")
                        print(f"ID: {staff['staff_id']}")
                        print(f"First Name: {staff['fname']}")
                        print(f"Last Name: {staff['lname']}")
                        print(f"Position: {staff['job']}")
                        print(f"Start Date: {staff['start']}")
                    else:
                        print("Sorry, couldn't find that staff member.")
                else:
                    print(f"Error: {error}")

            elif choice == '3':
                staff_id = input("Staff ID number: ").strip()
                new_fname = input("New first name: ").strip()
                new_lname = input("New last name: ").strip()
                update_employee = Employee(staff_id, new_fname, new_lname, "", "")
                success, error = update_employee.update()
                if success:
                    print("Name updated successfully!")
                else:
                    print(f"Error: {error}")

            elif choice == '4':
                staff_id = input("Staff ID to remove: ").strip()
                remove_employee = Employee(staff_id, "", "", "", "")
                success, error = remove_employee.remove()
                if success:
                    print("Staff member removed from system.")
                else:
                    print(f"Error: {error}")

            elif choice == '5':
                job = input("Job title: ").strip()
                base = float(input("Regular hourly rate: ").strip())
                weekend = float(input("Weekend hourly rate: ").strip())
                wage_manager.add_job_rate(job, base, weekend)
                print("New job pay rate added!")

            elif choice == '6':
                job = input("Job title to check: ").strip()
                rates = wage_manager.get_job_rate(job)
                if rates:
                    print(f"\nPay rates for {job}:")
                    print(f"Regular hours: ${rates['base']:.2f}")
                    print(f"Weekend hours: ${rates['weekend']:.2f}")
                else:
                    print("That job title isn't in our system.")

            elif choice == '7':
                job = input("Job title: ").strip()
                new_base = float(input("New regular rate: ").strip())
                new_weekend = float(input("New weekend rate: ").strip())
                wage_manager.update_job_rate(job, new_base, new_weekend)
                print("Pay rates updated!")

            elif choice == '8':
                job = input("Job title to remove: ").strip()
                wage_manager.remove_job_rate(job)
                print("Job pay rates removed.")

            elif choice == '9':
                employee_manager.show_staff_list()

            elif choice == '10':
                # Explicitly specify the sort field
                success, staff_report, error = reports.create_staff_list(sort_by="lname")
                if success:
                    reports.save_csv_report(staff_report, "staff_list")
                    print("Staff list report saved!")
                else:
                    print(f"Error: {error}")

            elif choice == '11':
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                emp_id = input("Enter employee ID: ").strip()
                
                success, schedule_report, error = reports.generate_employee_schedule(emp_id, start_date, end_date)
                if success:
                    success, msg = reports.save_csv_report(schedule_report, f"schedule_{emp_id}")
                    if success:
                        print("Schedule report saved successfully!")
                    else:
                        print(f"Error saving report: {msg}")
                else:
                    print(f"Error generating report: {error}")

            elif choice == '12':
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                
                success, wage_report, error = reports.generate_wage_report(start_date, end_date)
                if success:
                    success, msg = reports.save_csv_report(wage_report, "wage_report")
                    if success:
                        print("Wage report saved successfully!")
                    else:
                        print(f"Error saving report: {msg}")
                else:
                    print(f"Error generating report: {error}")

            elif choice == '13':
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                
                success, wage_report, error = reports.generate_wage_report(start_date, end_date)
                if success:
                    success, msg = reports.save_text_report(
                        wage_report, 
                        "wage_report", 
                        f"Wage Report ({start_date} to {end_date})"
                    )
                    if success:
                        print("Wage report saved successfully!")
                    else:
                        print(f"Error saving report: {msg}")
                else:
                    print(f"Error generating report: {error}")

            elif choice == '14':
                print("Thanks for using the system. Goodbye!")
                break

            else:
                print("Oops! Please choose a number from 1-14.")

        except ValueError as e:
            print(f"Input error: {e}")
        except Exception as e:
            print(f"Something went wrong: {e}")

if __name__ == "__main__":
    run_system()
