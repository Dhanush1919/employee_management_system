from connection import conn
from datetime import datetime
import re
import mysql.connector 
import pandas as pd
import os 

### Option 1 - Adding Employee Details
def add_employee(name,age,address,mobile_number,gender,education_details,doj,department,position):
    cursor = conn.cursor()

    sql = "INSERT INTO employee_details (name,age,address,mobile_number,gender,education_details,doj,department,position) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
    values = (name,age,address,mobile_number,gender,education_details,doj,department,position)

    cursor.execute(sql, values)
    conn.commit()

    print("Employee detail added")

### Option 2 - Viewing Employee details using Name
def view_employee_details(name):
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM employee_details WHERE name = %s",(name,))
    employee_details = cursor.fetchone()

    if employee_details:
        print("Employee Details :")
        for column, value in zip(cursor.column_names, employee_details):
            print(f"{column.capitalize()}: {value}")
    else:
        print("No Employee found")

### Option 3 - Updating existing employees information 
def updating_employee_info(s_name, **fields):
    cursor = conn.cursor()
    # Check if the employee exists
    cursor.execute("SELECT * FROM employee_details WHERE name = %s", (s_name,))
    student = cursor.fetchone()
    if student is None:
        print("Error: Student not found.")
        return

    # Check if 'name' column is included in kwargs
    if 'name' in fields:
        print("Error: Name cannot be updated.")
        return

    # Prepare the update query
    update_query = "UPDATE employee_details SET "
    update_values = []
    for key, value in fields.items():
        update_query += f"{key} = %s, "
        update_values.append(value)
    if not update_values:
        print("Error: No valid columns to update.")
        return
    update_query = update_query.rstrip(", ") + " WHERE name = %s"
    update_values.append(s_name)

    # Execute the update query
    cursor.execute(update_query, update_values)
    conn.commit()
    print("Employee information updated successfully!")

### OPTION 4 - DELETE EMPLOYEE RECORD - HAS TO BE FIXED 
def delete_employee_details(s_name):
    cursor = conn.cursor()

    ### CHECKING IF THE EMPLOYEE EXISTS :
    cursor.execute("SELECT * FROM employee_details WHERE name = %s",(s_name,))
    employee = cursor.fetchone()

    if employee is None:
        print("Employee does not exist !! ")
        return 
    
    deletion_query = "UPDATE employee_details SET soft_delete = 1 WHERE name = %s",(s_name,)

    cursor.execute(deletion_query)

### OPTION 5 - DISPLAYING ALL THE EMPLOYEES BASED ON DEPARTMENT, POSITION AND GENDER  
def display_employee(dep_name,position,gender):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employee_details WHERE department = %s AND position = %s AND gender = %s",(dep_name,position,gender))
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
    output_file = os.path.join(file_path, f'{table_name}_output.csv')
    df.to_csv(output_file, index=False)

    # Close the cursor and connection
    cursor.close()
    conn.close()

### OPTION 8 - IMPORTING DATA FROM A CSV FILE :
def import_data(csv_file_path,file_name,table_name):
    cursor = conn.cursor()
    print("The path of the file is : ", csv_file_path)
    
    file_path = csv_file_path+'/'+file_name

    df = pd.read_csv(file_path)

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

