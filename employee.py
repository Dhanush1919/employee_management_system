from connection import conn
from datetime import datetime
import re
import mysql.connector 


### INSERTING DATA INTO STUDENTS DATA :
def insert_students_from_df(df):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        sql = "INSERT INTO employee_details(name,age,address,mobile_number,gender,education_details,doj,department,position) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
        values = (row['name'],row['age'],row['address'],row['mobile_number'],row['gender'],row['education_details'],row['doj'],row['department'],row['position'])
        cursor.execute(sql, values)
        conn.commit()
    
def test():
    print("Testing")

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