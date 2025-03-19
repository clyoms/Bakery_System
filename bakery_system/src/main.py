from pathlib import Path
from employee_data import add_employee, get_employee_by_id, update_employee_name, delete_employee, initialize_employee_file, print_employee_data
from wage_data import add_position_rate, get_position_rate, update_position_rate, delete_position_rate, initialize_wage_file

# Initialize files and directories
initialize_employee_file()
initialize_wage_file()

# CLI Menu
def print_menu():
    print("\nEmployee Management System")
    print("1. Add Employee")
    print("2. View Employee")
    print("3. Update Employee Name")
    print("4. Delete Employee")
    print("5. Add Position Rate")
    print("6. View Position Rate")
    print("7. Update Position Rate")
    print("8. Delete Position Rate")
    print("9. Show Employee Data")
    print("10. Exit")

# Main function to handle user input and actions
def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip().lower()

        try:
            if choice == '1':  # Add Employee
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                position = input("Enter position: ")
                start_date = input("Enter start date (DD-MM-YYYY): ")
                add_employee(first_name, last_name, position, start_date)
                print(f"Employee added successfully!")

            elif choice == '2':  # View Employee
                employee_id = input("Enter employee ID: ")
                employee = get_employee_by_id(employee_id)
                if employee:
                    print(f"Employee details: {employee}")
                else:
                    print("Employee not found.")

            elif choice == '3':  # Update Employee Name
                employee_id = input("Enter employee ID: ")
                new_first_name = input("Enter new first name: ")
                new_last_name = input("Enter new last name: ")
                update_employee_name(employee_id, new_first_name, new_last_name)
                print(f"Employee name updated successfully!")

            elif choice == '4':  # Delete Employee
                employee_id = input("Enter employee ID: ")
                delete_employee(employee_id)
                print(f"Employee deleted successfully!")

            elif choice == '5':  # Add Position Rate
                position = input("Enter position: ")
                base_rate = float(input("Enter base rate: "))
                weekend_rate = float(input("Enter weekend rate: "))
                add_position_rate(position, base_rate, weekend_rate)
                print(f"Position rate added successfully!")

            elif choice == '6':  # View Position Rate
                position = input("Enter position: ")
                rate = get_position_rate(position)
                if rate:
                    print(f"Position rate: {rate}")
                else:
                    print("Position not found.")

            elif choice == '7':  # Update Position Rate
                position = input("Enter position: ")
                new_base_rate = float(input("Enter new base rate: "))
                new_weekend_rate = float(input("Enter new weekend rate: "))
                update_position_rate(position, new_base_rate, new_weekend_rate)
                print(f"Position rate updated successfully!")

            elif choice == '8':  # Delete Position Rate
                position = input("Enter position: ")
                delete_position_rate(position)
                print(f"Position rate deleted successfully!")

            elif choice == '9':
                print_employee_data()

            elif choice == '10':  # Exit
                print("Exiting system.")
                break

            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()