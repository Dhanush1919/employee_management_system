from employee import *
from connection import conn
from login_validation  import authentication

# Define the menu function
def display_menu():
    print("Features to choose")
    print("1. Add a New Employee")
    print("2. View a Particular Employees details")
    print("3. Update Employee Information")
    print("4. Delete an Employee record")
    print("5. List all employees in the organization")
    print("6. Calculate total salary at monthly level of each employee")
    print("7. Export employee data to a CSV file")
    print("8. Import employee data from a CSV file")
    print("9. Add tech stack for employees")
    print("10. View employee's known tech stack (applicable only for engineering employees)")
    print("11. Search employees by name")
    print("12. Search employees by tech stack")
    print("13. Search employees by project name")
    option = int(input('Enter the feature to be chosen :'))
    return option

def main():
    if 

if __name__ == "__main__":
    main()