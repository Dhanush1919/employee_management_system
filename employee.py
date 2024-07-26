from connection import conn
from datetime import datetime
import re
import mysql.connector 


### INSERTING DATA INTO STUDENTS DATA :
def insert_students_from_df(df):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        sql = "INSERT INTO students (name,age,address,mobile_number,gender,education_details,doj,department,position,project) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
        values = (row['name'],row['age'],row['address'],row['mobile_number'],row['gender'],row['education_details'],row['doj'],row['department'],row['position'],row['project'])
        cursor.execute(sql, values)
        conn.commit()



