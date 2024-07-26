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
    if not authentication():
        print("Invalid Username or Password")
        return 
    
    cursor = conn.cursor()
    while True:

        option = display_menu()
        if option == 0:
            break 
    
        elif(option==1):
             name = input('Enter the name of the employee : ')
             age = input('Enter the age of the employee : ')
             address = input('Enter the address of the employee : ')
             mobile_number = input('Enter the mobile number of the employee : ')
             gender = input('Enter the gender of employee : ')
             education_details = input('Enter the education details of employee : ')
             doj = input('Enter the DOJ (In YYYY-MM-DD format) of employee : ')
             department = input('Enter the department of employee : ')
             position = input('Enter the position of employee : ')
             ### project = input('Enter the project of employee : ')
             add_employee(name,age,address,mobile_number,gender,education_details,doj,department,position)
        
        elif(option==2):
            name = input('Enter the name of the employee to view their details : ')
            view_employee_details(name)



if __name__ == "__main__":
    main()