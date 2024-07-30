from connection import conn
from datetime import datetime
import re
import mysql.connector 
import pandas as pd
import os 

### OPTION 1 - ADD EMPLOYEE DETAILS 
def add_employee(Employee_ID,Name,Age,Address,Mobile_number,Gender,Education_details,Doj,Department,Position,Project_ID,Project_name,Project_assigned_date,Manager_ID,Tech_stack,Employees_known_tech_stack,Employee_salary):
    cursor = conn.cursor()

    sql = "INSERT INTO employee_data (Employee_ID,Name,Age,Address,Mobile_number,Gender,Education_details,Doj,Department,Position,Project_ID,Project_name,Project_assigned_date,Manager_ID,Tech_stack,Employees_known_tech_stack,Employee_salary) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (Employee_ID,Name,Age,Address,Mobile_number,Gender,Education_details,Doj,Department,Position,Project_ID,Project_name,Project_assigned_date,Manager_ID,Tech_stack,Employees_known_tech_stack,Employee_salary)

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

    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nineleaps",
    database="employee_management_system_schema"
    )

    cursor = conn.cursor()

    ### CHECKING IF THE EMPLOYEE EXISTS :
    cursor.execute("SELECT * FROM employee_data WHERE Employee_ID = %s",(Employee_ID,))
    employee = cursor.fetchone()

    if employee is None:
        print("Employee does not exist !! ")
        return 
    
    deletion_query = "DELETE FROM employee_data WHERE Employee_ID = %s",(Employee_ID,)

    cursor.execute(deletion_query)
    cursor.close()


### OPTION 5 - DISPLAYING ALL THE EMPLOYEES BASED ON DEPARTMENT, POSITION AND GENDER  
def display_employee(Department,Position,Gender):
    cursor = conn.cursor()

    cursor.execute("SELECT Employee_ID,Name,Age FROM employee_data WHERE Department = %s AND Position = %s AND Gender = %s",(Department,Position,Gender))
    employee_data = cursor.fetchall()

    for i in employee_data:
        print(i)

### OPTION 6 - CALCULATING TOTAL SALARY ON MONTH LEVEL OF EACH EMPLOYEE 



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
    cursor.close()
    conn.close()

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

### OPTION 15 - 

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

    search_query = "SELECT * FROM employee_data WHERE tech_stack = %s"

    cursor.execute(search_query, (t_stack,))

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

    if cursor:
        cursor.close()
