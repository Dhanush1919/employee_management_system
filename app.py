import streamlit as st
from employee import *
from connection import conn
from login_validation import authentication

def main():
    st.title("Employee Management System")

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "nineleaps" and password == "nineleaps":
                st.session_state.authenticated = True
                st.success("Login successful")
            else:
                st.error("Invalid Username or Password")
        return

    menu_options = [
        "Add New Employee Details",
        "View Employee Details",
        "Update Employee Information",
        "Delete Employee Details",
        "List All Employees",
        "Calculate Total Salary",
        "Export Data to CSV",
        "Import Data from CSV",
        "Assign Project to Employees",
        "View Employee's Project Details",
        "Update Employee's Project Details",
        "Assign Manager to Employees",
        "View Manager Details",
        "Add Tech Stack for Employees",
        "View Employee's Known Tech Stack",
        "Search Employees by Name",
        "Search Employees by Tech Stack",
        "Search Employees by Project",
        "Sort Employees by Salary"
    ]

    choice = st.sidebar.selectbox("Menu", menu_options)

    if choice == "Add New Employee Details":
        add_new_employee()
    elif choice == "View Employee Details":
        view_employee()
    elif choice == "Update Employee Information":
        update_employee()
    elif choice == "Delete Employee Details":
        delete_employee()
    elif choice == "List All Employees":
        list_all_emp()
    elif choice == "Calculate Total Salary":
        calculate_tot_salary()
    elif choice == "Export Data to CSV":
        exp_data()
    elif choice == "Import Data from CSV":
        imp_data()
    elif choice == "Assign Project to Employees":
        ass_project()
    elif choice == "View Employee's Project Details":
        view_pro_details()
    elif choice == "Update Employee's Project Details":
        update_proj_details()
    elif choice == "Assign Manager to Employees":
        ass_manager()
    elif choice == "View Manager Details":
        view_man_details()
    elif choice == "Add Tech Stack for Employees":
        add_tech_st()
    elif choice == "View Employee's Known Tech Stack":
        view_known_tech_st()
    elif choice == "Search Employees by Name":
        sea_by_name()
    elif choice == "Search Employees by Tech Stack":
        sea_by_tech_stack()
    elif choice == "Search Employees by Project":
        sea_by_project()
    elif choice == "Sort Employees by Salary":
        sort_by_salaries()

def add_new_employee():
    st.subheader("Add New Employee Details")
    Employee_ID = st.text_input('Enter the ID of the Employee')
    Name = st.text_input('Enter the Name of the Employee')
    Age = st.text_input('Enter the Age of the Employee')
    Address = st.text_input('Enter the Address of the Employee')
    Mobile_number = st.text_input('Enter the Mobile number of the Employee')
    Gender = st.text_input('Enter the Gender of the Employee')
    Education_details = st.text_input('Enter the Education details of the Employee')
    Doj = st.text_input('Enter the Date of Joining (DOJ) of the Employee')
    Department = st.text_input('Enter the Department of the Employee')
    Position = st.text_input('Enter the Position of the Employee')
    Project_ID = st.text_input('Enter the Project ID of the Employee')
    Project_name = st.text_input('Enter the Project name of the Employee')
    Project_assigned_date = st.text_input('Enter the Project assigned date of the Employee')
    Manager_ID = st.text_input('Enter the Manager ID of the Employee')
    Employees_known_tech_stack = st.text_input('Enter the Employees known tech stack of the Employee')
    Employee_salary = st.text_input('Enter the Employee salary of the Employee')
    
    if st.button('Add Employee'):
        add_employee(Employee_ID, Name, Age, Address, Mobile_number, Gender, Education_details, Doj, Department, Position, Project_ID, Project_name, Project_assigned_date, Manager_ID, Employees_known_tech_stack, Employee_salary)
        st.success('Employee added successfully')

def view_employee():
    st.subheader("View Employee Details")
    Employee_ID = st.text_input('Enter the ID of the employee to view their details')
    if st.button('View Employee'):
        employee_details = view_employee_details(Employee_ID)
        if employee_details:
            for detail in employee_details:
                st.write(detail)
        else:
            st.error("Employee not found")

def update_employee():
    st.subheader("Update Employee Information")
    Employee_ID = st.text_input('Enter the ID of the Employee')
    fields_to_update = {}
    
    field = st.text_input("Enter the Field name that you wish to update")
    value = st.text_input(f"Enter new value for {field}")
    if field and value:
        fields_to_update[field] = value
    
    if st.button('Update Employee'):
        updating_employee_info(Employee_ID, **fields_to_update)
        st.success('Employee updated successfully')

def delete_employee():
    st.subheader("Delete Employee Details")
    Employee_ID = st.text_input('Enter the ID of the Employee you want to delete')
    if st.button('Delete Employee'):
        delete_employee_details(Employee_ID)
        st.success('Employee deleted successfully')

def list_all_emp():
    st.subheader("List All Employees")
    dep_name = st.text_input('Enter the name of the department')
    position = st.text_input('Enter the position of the employee')
    gender = st.text_input('Enter the gender of the employee')

    if st.button('List Employees'):
        employees = display_employee(dep_name, position, gender)
        for emp in employees:
            st.write(emp)

def calculate_tot_salary():
    st.subheader("Calculate Total Salary at Month Level")
    if st.button('Calculate'):
        salary = month_wise_salary()
        st.write(f"Total Salary: {salary}")

def exp_data():
    st.subheader("Export Data to CSV")
    table_name = st.text_input('Enter the name of the table (employee_data, manage_details, project_assigned_details) you want to export data')
    if st.button('Export'):
        expo_data(table_name)
        st.success("Data exported successfully")

def imp_data():
    st.subheader("Import Data from CSV")
    csv_file_path = st.text_input('Enter the path of the CSV')
    file_name = st.text_input('Enter the name of the file')
    table_name = st.text_input('Enter the name of the table')

    if st.button('Import'):
        import_data(csv_file_path, file_name, table_name)
        st.success("Data imported successfully")

def ass_project():
    st.subheader("Assign Project to Employees")
    if st.button('Assign'):
        assign_project_to_each_employee()
        st.success("Project assigned successfully")

def view_pro_details():
    st.subheader("View Employee's Project Details")
    emp_id = st.text_input('Enter the ID of the employee to view their projects')
    if st.button('View'):
        project_details = view_project_details(emp_id)
        for detail in project_details:
            st.write(detail)

def update_proj_details():
    st.subheader("Update Employee's Project Details")
    emp_id = st.text_input('Enter the ID of the Employee')
    project_id = st.text_input('Enter the ID of the Project')
    project_name = st.text_input('Enter the Name of the Project')
    project_desc = st.text_input('Enter the description of the Project')
    if st.button('Update'):
        updating_employee_project_details(emp_id, project_id, project_name, project_desc)
        st.success('Employee project details updated successfully')

def ass_manager():
    st.subheader("Assign Manager to Employees")
    table_name = st.text_input('Enter the Employee Table name')
    if st.button('Assign'):
        assign_manager_to_each_employees()
        st.success("Manager assigned successfully")

def view_man_details():
    st.subheader("View Manager's Details of an Employee")
    emp_id = st.text_input('Enter the ID of the Employee to view their manager details')
    if st.button('View'):
        manager_details = view_manager_details(emp_id)
        for detail in manager_details:
            st.write(detail)

def add_tech_st():
    st.subheader("Add Tech Stack for Employees")
    emp_id = st.text_input('Enter the ID of the Employee')
    tech_stack = st.text_input('Enter the Tech stack of Employee')
    if st.button('Add'):
        adding_tech_stack(emp_id, tech_stack)
        st.success('Tech stack added successfully')

def view_known_tech_st():
    st.subheader("View Employee's Known Tech Stack")
    department_name = st.text_input('Enter the name of the Department you want to check for')

    if st.button('View'):
        if department_name == 'Engineering':
            tech_stacks = view_employees_known_tech_stack(department_name)
            for stack in tech_stacks:
                st.write(stack)
        else:
            st.error("Invalid Department Entry")

def sea_by_name():
    st.subheader("Search Employees by Name")
    e_name = st.text_input('Enter the name of the Employee to search for')
    if st.button('Search'):
        employees = searching_using_name(e_name)
        for emp in employees:
            st.write(emp)

def sea_by_tech_stack():
    st.subheader("Search Employees by Tech Stack")
    t_stack = st.text_input('Enter the tech stack')
    if st.button('Search'):
        employees = searching_using_tech_stack(t_stack)
        for emp in employees:
            st.write(emp)

def sea_by_project():
    st.subheader("Search Employees by Project Name")
    p_name = st.text_input('Enter the name of the Project')
    if st.button('Search'):
        employees = searching_using_project(p_name)
        for emp in employees:
            st.write(emp)

def sort_by_salaries():
    st.subheader("Sort Employees by Salary")
    sort_type = st.text_input('Enter the sort type (ascending/descending)')
    if st.button('Sort'):
        employees = sorting_records(sort_type)
        for emp in employees:
            st.write(emp)

if __name__ == "__main__":
    main()
