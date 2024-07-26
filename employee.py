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

def add_employee(name,age,address,mobile_number,gender,education_details,doj,department,position):
    cursor = conn.cursor()

    sql = "INSERT INTO employee_details (name,age,address,mobile_number,gender,education_details,doj,department,position) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
    values = (name,age,address,mobile_number,gender,education_details,doj,department,position)

    cursor.execute(sql, values)
    conn.commit()

    print("Employee detail added")

def view_employee_details(name):
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM employee_details WHERE name = %s,"(name))
    employee_details = cursor.fetchone()

    if employee_details:
        print("Employee Details :")
        for column, value in zip(cursor.column_names, employee_details):
            print(f"{column.capitalize()}: {value}")
    else:
        print("No Employee found")


