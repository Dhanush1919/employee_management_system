from connection import conn
from datetime import datetime
import re
import mysql.connector 
import pandas as pd
import os 

### OPTION 1 - ADD EMPLOYEE DETAILS 
def add_employee(Employee_ID,Name,Age,Address,Mobile_number,Gender,Education_details,Doj,Department,Position,Project_ID,Project_name,Project_assigned_date,Manager_ID,Employees_known_tech_stack,Employee_salary):
    cursor = conn.cursor()

    sql = "INSERT INTO employee_data (Employee_ID,Name,Age,Address,Mobile_number,Gender,Education_details,Doj,Department,Position,Project_ID,Project_name,Project_assigned_date,Manager_ID,Employees_known_tech_stack,Employee_salary) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (Employee_ID,Name,Age,Address,Mobile_number,Gender,Education_details,Doj,Department,Position,Project_ID,Project_name,Project_assigned_date,Manager_ID,Employees_known_tech_stack,Employee_salary)

    cursor.execute(sql, values)
    conn.commit()

    print("Employee detail added")

### OPTION 2 - VIEWING EMPLOYEE DETAILS USING EMPLOYEE_ID 
def view_employee_details(Employee_ID):
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM employee_data WHERE Employee_ID = %s",(Employee_ID,))
    employee_details = cursor.fetchone()

    if employee_details:
        print("Employee Details :")
        for column, value in zip(cursor.column_names, employee_details):
            print(f"{column.capitalize()}: {value}")
    else:
        print("No Employee found")

### Option 3 - Updating existing employees information 
def updating_employee_info(s_id, **fields):
    cursor = conn.cursor()
    # Check if the employee exists
    cursor.execute("SELECT * FROM employee_data WHERE Employee_ID = %s", (s_id,))
    student = cursor.fetchone()
    if student is None:
        print("Error: Student not found.")
        return

    # Check if 'name' column is included in kwargs
    if 'Name' in fields:
        print("Error: Name cannot be updated.")
        return

    # Prepare the update query
    update_query = "UPDATE employee_data SET "
    update_values = []
    for key, value in fields.items():
        update_query += f"{key} = %s, "
        update_values.append(value)
    if not update_values:
        print("Error: No valid columns to update.")
        return
    update_query = update_query.rstrip(", ") + " WHERE Employee_ID = %s"
    update_values.append(s_id)

    # Execute the update query
    cursor.execute(update_query, update_values)
    conn.commit()
    print("Employee information updated successfully!")

### OPTION 4 - DELETE EMPLOYEE RECORD
def delete_employee_details(Employee_ID):

    cursor = conn.cursor()

    # CHECKING IF THE EMPLOYEE EXISTS:
    cursor.execute("SELECT * FROM employee_data WHERE Employee_ID = %s", (Employee_ID,))
    employee = cursor.fetchone()

    if employee is None:
        print("Employee does not exist !!")
        cursor.close()
        conn.close()  # Close the connection if the employee does not exist
        return 

    # Deletion query
    deletion_query = "DELETE FROM employee_data WHERE Employee_ID = %s"
    cursor.execute(deletion_query, (Employee_ID,))

    # Commit the transaction
    conn.commit()

    print("Employee deleted successfully.")

    ### cursor.close()
    ### conn.close()


### OPTION 5 - DISPLAYING ALL THE EMPLOYEES BASED ON DEPARTMENT, POSITION AND GENDER  
def display_employee(Department,Position,Gender):
    cursor = conn.cursor()

    cursor.execute("SELECT Employee_ID,Name,Age FROM employee_data WHERE Department = %s AND Position = %s AND Gender = %s",(Department,Position,Gender))
    employee_data = cursor.fetchall()

    for i in employee_data:
        print(i)

### OPTION 6 - CALCULATING TOTAL SALARY ON MONTH LEVEL OF EACH EMPLOYEE 
def month_wise_salary():

    cursor = conn.cursor()

    month_wise_salary_query = """
    SELECT
        DATE_FORMAT(Doj, '%Y-%m') AS joining_month,
        SUM(Employee_salary) AS total_salary
    FROM
        employee_data
    GROUP BY
        joining_month
    ORDER BY
        joining_month
    """

    cursor.execute(month_wise_salary_query)
    result = cursor.fetchall()

    for i in result:
        print(i)

### OPTION 7 - EXPORTING DATA TO CSV FILE :
def expo_data(table_name):
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    column_names = [i[0] for i in cursor.description]

    df = pd.DataFrame(rows, columns=column_names)

    ### CONVERTING THE DATAFRAME INTO A CSV AND EXPORTING IT  
    file_path = '/home/nineleaps/Downloads'
    output_file = os.path.join(file_path, f'{table_name}_exported.csv')
    df.to_csv(output_file, index=False)

    # Close the cursor and connection
    ### cursor.close()
    ### conn.close()

### OPTION 8 - IMPORTING DATA FROM A CSV FILE :
def import_data(csv_file_path,file_name,table_name):
    cursor = conn.cursor()
    
    file_path = csv_file_path+'/'+file_name

    df = pd.read_csv(file_path)

    print(f"Preview of the 1st five records which will be inserted into {table_name}")
    print(df.head())

    columns = df.columns.tolist()

    # Construct the SQL INSERT statement dynamically
    placeholders = ', '.join(['%s'] * len(columns))
    columns = ', '.join(columns)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Convert DataFrame rows to list of tuples
    data = [tuple(row) for row in df.to_numpy()]

    # Execute the SQL statement for each row
    cursor.executemany(sql, data)
    
    # Commit the transaction
    conn.commit()

### OPTION 9 - ASSIGNING PROJECTS TO EACH EMPLOYEE : 
def assign_project_to_each_employee():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="nineleaps",
            database="employee_management_system_schema"
        )
        cursor = db_connection.cursor()

        # Step 1: Create a temporary table to store the latest projects for each employee
        print("Creating temporary table...")
        create_temp_table_query = """
        CREATE TEMPORARY TABLE latest_projects AS
        SELECT
            Employee_ID,
            Project_ID,
            Project_name,
            Project_assigned_date
        FROM
            project_assigned_details
        WHERE
            (Employee_ID, Project_assigned_date) IN (
                SELECT
                    Employee_ID,
                    MAX(Project_assigned_date)
                FROM
                    project_assigned_details
                GROUP BY
                    Employee_ID
            );
        """
        cursor.execute(create_temp_table_query)
        cursor.execute("SELECT * FROM latest_projects;")
        latest_projects = cursor.fetchall()
        print(f"Temporary table created with {len(latest_projects)} records.")

        # Step 2: Update the employee_data table with the latest project details
        print("Updating employee_data with latest project details...")
        update_employee_data_query = """
        UPDATE employee_data e
        JOIN latest_projects lp ON e.Employee_ID = lp.Employee_ID
        SET
            e.Project_ID = lp.Project_ID,
            e.Project_name = lp.Project_name,
            e.Project_assigned_date = lp.Project_assigned_date;
        """
        cursor.execute(update_employee_data_query)
        db_connection.commit()
        print(f"Employee data updated: {cursor.rowcount} rows affected.")

        # Step 3: Handle employees without any project assignments
        print("Updating employees without projects to default values...")
        update_training_query = """
        UPDATE employee_data
        SET
            Project_ID = 1111,
            Project_name = 'Training',
            Project_assigned_date = Doj
        WHERE
            Project_ID IS NULL OR Project_name IS NULL OR Project_assigned_date IS NULL;
        """
        cursor.execute(update_training_query)
        db_connection.commit()
        print(f"Employees updated to default values: {cursor.rowcount} rows affected.")

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")

    ###finally:
        # Close the cursor and connection
        ### if cursor:
            ### cursor.close()
        ### if db_connection:
            ### db_connection.close()

    print("Employee data update process completed.")

### OPTION 10 - VIEW EMPLOYEE'S PROJECT DETAILS :
def view_project_details(emp_id):
    cursor = conn.cursor()

    employee_project_details = """
    SELECT 
        Employee_ID,
        project_id,
        project_name,
        project_description,
        project_start_date,
        project_end_date
        project_assigned_date
    FROM employee_management_system_schema.project_assigned_details EP

    WHERE EP.Employee_ID = %s
    """

    cursor.execute(employee_project_details,(emp_id,))
    result = cursor.fetchall()

    for i in result:
        print(i)

### OPTION 11 - UPDATING EMPLOYEES PROJECT DETAILS :
def updating_employee_project_details(emp_id,project_id,project_name,project_desc):
    
    cursor = conn.cursor()
    
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Check if the employee_id is present and has a project with project_end_date as NULL
    check_query = """
    SELECT * FROM project_assigned_details
    WHERE Employee_ID = %s AND Project_end_date IS NULL;
    """
    cursor.execute(check_query, (emp_id,))
    current_project = cursor.fetchone()

    if current_project:
        # Update the current project to set the project_end_date to today's date
        update_query = """
        UPDATE project_assigned_details
        SET Project_end_date = %s
        WHERE Employee_ID = %s AND Project_end_date IS NULL;
        """
        cursor.execute(update_query, (current_date, emp_id))
        print(f"Updated current project for employee {emp_id}.")

    # Insert the new project assignment
    insert_query = """
    INSERT INTO project_assigned_details (
        Project_ID, Project_name, Project_description, Project_start_date, Project_end_date, Employee_ID
    ) VALUES (%s, %s, %s, %s, NULL, %s);
    """
    cursor.execute(insert_query, (project_id, project_name, project_desc, current_date, emp_id))
    print(f"Inserted new project assignment for employee {emp_id}.")

    #### NEWLY ADDED

    current_date = datetime.now().strftime('%Y-%m-%d')

    # Update the project details in the employee_data table
    update_employee_data_query = """
    UPDATE employee_data
    SET project_id = %s, project_name = %s, project_assigned_date = %s
    WHERE Employee_ID = %s;
    """
    cursor.execute(update_employee_data_query, (project_id, project_name, current_date, emp_id))
    print(f"Updated employee_data table for employee {emp_id}.")
    #### NEWLY ADDED


    # Commit the transaction to save the changes
    conn.commit()

    ### if cursor:
        ### cursor.close()


### OPTION 12 - ASSIGNING A MANAGER TO EACH EMPLOYEE :
def assign_manager_to_each_employees():
    cursor = conn.cursor()

    update_manager_id_query = """
    UPDATE employee_data e
    JOIN manager_details m ON e.Employee_ID = m.Employee_ID
    SET e.Manager_ID = m.Manager_ID;
    """
    cursor.execute(update_manager_id_query)

    conn.commit()

    print(f"Employee data updated: {cursor.rowcount} rows affected.")

    ### if cursor:
        ### cursor.close()

### OPTION 13 - VIEW EMPLOYEE'S MANAGER DETAILS :
def view_manager_details(emp_id):
    cursor = conn.cursor()

    manager_details = """
    SELECT
        m.Manager_name, 
        COUNT(e.Employee_ID) AS Reportee_Count 
    FROM 
        manager_details m 
    INNER JOIN 
        manager_details e 
    ON 
        m.Manager_ID = e.Manager_ID 
    WHERE 
        e.Employee_ID = %s
    GROUP BY 
        m.Manager_id,
        m.Manager_name
    """
    cursor.execute(manager_details, (emp_id,))
    result = cursor.fetchone()

    if result:
        manager_name, reportee_count = result[:2]
        print(f"Manager Name: {manager_name}, Number of Reportees: {reportee_count}")
    else:
        print("No manager details found for the given employee ID.")

### OPTION 14 - ADDING TECH STACK FOR EMPLOYEES : 
def adding_tech_stack(emp_id,tech_stack):
    
    cursor = conn.cursor()

    # First, fetch the current tech stack of the employee
    fetch_query = "SELECT Employees_known_tech_stack FROM employee_data WHERE Employee_ID = %s"
    
    cursor.execute(fetch_query, (emp_id,))
    
    current_tech_stack = cursor.fetchone()
    
    if current_tech_stack:
        current_tech_stack = current_tech_stack[0]
        
        # Append the new tech stack to the existing one, if it's not empty
        if current_tech_stack:
            new_tech_stack = current_tech_stack + ", " + tech_stack
        else:
            new_tech_stack = tech_stack
        
        # Update the tech stack in the database
        update_query = "UPDATE employee_data SET Employees_known_tech_stack = %s WHERE Employee_ID = %s"
        cursor.execute(update_query, (new_tech_stack, emp_id))

        conn.commit()
        print(f"Updated tech stack for Employee ID {emp_id} to: {new_tech_stack}")
    else:
        print(f"Employee ID {emp_id} not found.")

    
    ### if cursor:
        ### cursor.close()

### OPTION 15 -  VIEW EMPLOYEE'S TECH STACK :
def view_employees_known_tech_stack(department_name):
    cursor = conn.cursor()

    view_employees_tech_stack = "SELECT Employee_Id,Employees_known_tech_stack, Department FROM employee_data WHERE Department = %s"

    cursor.execute(view_employees_tech_stack,(department_name,))
    
    tech_stack_data = cursor.fetchall()

    for i in tech_stack_data:
        print(i)

### OPTION 16 - SEARCHING EMPLOYEES BY NAME :
def searching_using_name(e_name):
    cursor = conn.cursor()

    search_query = "SELECT * FROM employee_data WHERE Name = %s"

    cursor.execute(search_query, (e_name,))

    employee_data = cursor.fetchall()

    for i in employee_data:
        print(i)

### OPTION 17 - SEARCHING EMPLOYEES BY TECH STACK :
def searching_using_tech_stack(t_stack):
    cursor = conn.cursor()

    search_query = "SELECT * FROM employee_data WHERE Employees_known_tech_stack LIKE %s"

    cursor.execute(search_query, ('%' + t_stack + '%',))

    employee_data = cursor.fetchall()

    for i in employee_data:
        print(i)

### OPTION 18 - SEARCHING EMPLOYEES BY PROJECT :
def searching_using_project(p_name):
    cursor = conn.cursor()

    search_query = "SELECT * FROM employee_data WHERE project_name = %s"

    cursor.execute(search_query, (p_name,))

    employee_data = cursor.fetchall()

    for i in employee_data:
        print(i)
    
### OPTION 19 - SORT EMPLOYEES BY SALARY :
def sorting_records(sort_type):
    cursor = conn.cursor() 

    # Query to fetch and sort records by Employee_salary
    query = f"SELECT * FROM employee_data ORDER BY Employee_salary {sort_type}"

    # Execute the query
    cursor.execute(query)

    # Fetch all the sorted records
    sorted_records = cursor.fetchall()

    column_names = [i[0] for i in cursor.description]
    print(column_names)

    for record in sorted_records:
        print(record)

    ### if cursor:
        ### cursor.close()
