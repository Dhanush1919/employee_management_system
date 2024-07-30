from employee import *
from connection import conn
from login_validation  import authentication

# Define the menu function
def display_menu():
    print("1. ADD NEW EMPLOYEE DETAILS")
    print("2. TO VIEW EMPLOYEE DETAILS USING EMPLOYEE_ID")
    print("3. UODATE EMPLOYEE INFORMATION (NAME CAN'T BE UPDATED)")
    print("4. DELETING EMPLOYEE DETAILS FROM TABLE USING EMPLOYEE ID")
    print("5. LISTING ALL EMPLOYEES IN ORGANIZATION")
    print("6. CALCULATING TOTAL SALARY AT MONTH LEVEL OF EACH EMPLOYEE ")
    print("7. EXPORTING DATA TO A CSV FILE")
    print("8. IMPORTING DATA FROM A CSV FILE")
    print("16. SEARCHING EMPLOYEES BY NAME")
    print("17. SEARCHING EMPLOYEES BY TECH STACK")
    print("18. SEARCHING EMPLOYEES BY PROJECT")
    print("19. SORTING EMPLOYEES BY SALARY")
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
    
        ### OPTION 1 - ADD EMPLOYEE DETAILS 
        elif(option==1):
            Employee_ID = input('Enter the ID of the Employee : ')
            Name = input('Enter the Name of the Employee : ')
            Age = input('Enter the Age of the Employee : ')
            Address = input('Enter the Address of the Employee : ')
            Mobile_number = input('Enter the Mobile_number of the Employee : ')
            Gender = input('Enter the Gender of the Employee : ')
            Education_details = input('Enter the Education_details of the Employee : ')
            Doj = input('Enter the Doj of the Employee : ')
            Department = input('Enter the Department of the Employee : ')
            Position = input('Enter the Position of the Employee : ')
            Project_ID = input('Enter the Project_ID of the Employee : ')
            Project_name = input('Enter the Project_name of the Employee : ')
            Project_assigned_date = input('Enter the Project_assigned_date of the Employee : ')
            Manager_ID = input('Enter the Manager_ID of the Employee : ')
            Tech_stack = input('Enter the Tech_stack of the Employee : ')
            Employees_known_tech_stack = input('Enter the Employees_known_tech_stack of the Employee : ')
            Employee_salary = input('Enter the Employee_salary of the Employee : ')
            add_employee(Employee_ID,Name,Age,Address,Mobile_number,Gender,Education_details,Doj,Department,Position,Project_ID,Project_name,Project_assigned_date,Manager_ID,Tech_stack,Employees_known_tech_stack,Employee_salary)
        
        ### OPTION 2 - VIEWING EMPLOYEE DETAILS USING EMPLOYEE_ID 
        elif(option==2):
            Employee_ID = input('Enter the ID of the employee to view their details : ')
            view_employee_details(Employee_ID)

        ### Update employee information (name can’t be updated)
        elif(option==3):

            s_id = input('Enter the ID of the Student : ')
            fields_to_update = {}

            # Prompt the user for fields to update : 
            print("Enter the fields you want to update and their new values, or leave blank to stop:")
            while True:
                field = input("Enter the Field names that you wish to update or leave blank to stop: ").strip()
                if not field:
                    break
                value = input(f"Enter new value for {field}: ").strip()
                fields_to_update[field] = value
            updating_employee_info(s_id, **fields_to_update)

        ### DELETING EMPLOYEE DETAILS FROM TABLE :
        elif(option==4): ### NOT WORKING 

            Employee_ID = input('Enter the ID of the Employee you want to delete : ')
            delete_employee_details(Employee_ID)

        ### LISTING ALL EMPLOYEES IN ORGANIZATION : 
        elif(option==5):

            dep_name = input('Enter the name of the department : ')
            position = input('Enter the position of the employee : ')
            gender = input('Enter the gender of the employee : ')

            display_employee(dep_name,position,gender)

        ### CALCULATING TOTAL SALARY AT MONTH LEVEL OF EACH EMPLOYEE : 
        elif(option==6):
            pass 
    
        ### EXPORTING DATA TO A CSV FILE : 
        elif(option==7):
            
            table_name = input('Enter the name of the table (employee_data, manage_details, project_assigned_details) you want to export data : ')
            expo_data(table_name)
        
        ### IMPORTING DATA FROM A CSV FILE :
        elif(option==8):
            csv_file_path = input('Enter the path of the CSV : ')
            
            file_name = input('Enter the name of the file : ')
            
            table_name = input('Enter the name of the table : ')
            
            import_data(csv_file_path,file_name,table_name)

        ### ASSIGNING PROJECTS TO EACH EMPLOYEE :
        elif(option==9):
            assign_project_to_each_employee()
        
        ### VIEW MANAGER'S DETAILS OF AN EMPLOYEE :
        elif(option==13):
            emp_id = input('Enter the ID of the Employee to view their manager details : ')
            view_manager_details(emp_id)


        ### SEARCHING EMPLOYEES BY NAME :
        elif(option==16):
            e_name = input('Enter the name of the Employee to search for : ')
            searching_using_name(e_name)

        ### SEARCHING EMPLOYEES BY TECH STACK :
        elif(option==17):
            t_stack = input('Enter the tech stack : ')
            searching_using_tech_stack(t_stack)

        ### SEARCHING EMPLOYEES BY PROJECT NAME :
        elif(option==18):
            p_name = input('Enter the name of the Project : ')
            searching_using_project(p_name)

        ### SORT EMPLOYEES BY SALARY :
        elif(option==19):
            sort_type = input('Enter the type of Sort : ')
            sorting_records(sort_type)





if __name__ == "__main__":
    main()