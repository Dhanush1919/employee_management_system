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

# Function to add a new student with constraints
def add_employee(name,age,address,mobile_number,gender,education_details,doj,department,position):
    # Check if name and fathers_name contain special characters or numbers
    cursor = conn.cursor()

    # Insert SQL query
    sql = "INSERT INTO employee_details (name,age,address,mobile_number,gender,education_details,doj,department,position) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
    values = (name,age,address,mobile_number,gender,education_details,doj,department,position)

    # Execute SQL query
    cursor.execute(sql, values)
    conn.commit()

    print("Employee detail added")


