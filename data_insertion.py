import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Function to generate random data
def generate_random_employee():
    return {
        "Employee_ID": fake.unique.random_number(digits=5),
        "Name": fake.name(),
        "Age": random.randint(22, 60),
        "Address": fake.address(),
        "Mobile_number": fake.phone_number()[:15],  # Truncate to 15 characters
        "Gender": random.choice(["Male", "Female"]),
        "Education_details": fake.job(),
        "Doj": fake.date_between(start_date='-10y', end_date='today'),
        "Department": random.choice(["HR", "Engineering", "Marketing", "Sales"]),
        "Position": fake.job(),
        "Project_ID": fake.unique.random_number(digits=4),
        "Project_name": fake.word(),
        "Project_assigned_date": fake.date_between(start_date='-5y', end_date='today'),
        "Manager_ID": fake.random_number(digits=5),
        "Tech_stack": fake.word(),
        "Employees_known_tech_stack": fake.word(),
        "Employee_salary": round(random.uniform(30000, 120000), 2)
    }

# Connect to the MySQL database
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nineleaps",
        database="employee_management_system_schema"
    )
    cursor = db_connection.cursor()

    # Generate and insert random data
    num_records = 100  # Number of records to insert

    for _ in range(num_records):
        employee = generate_random_employee()
        insert_query = """
        INSERT INTO employee_data (
            Employee_ID, Name, Age, Address, Mobile_number, Gender, Education_details,
            Doj, Department, Position, Project_ID, Project_name, Project_assigned_date,
            Manager_ID, Tech_stack, Employees_known_tech_stack, Employee_salary
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            cursor.execute(insert_query, (
                employee["Employee_ID"], employee["Name"], employee["Age"], employee["Address"],
                employee["Mobile_number"], employee["Gender"], employee["Education_details"],
                employee["Doj"], employee["Department"], employee["Position"],
                employee["Project_ID"], employee["Project_name"], employee["Project_assigned_date"],
                employee["Manager_ID"], employee["Tech_stack"], employee["Employees_known_tech_stack"],
                employee["Employee_salary"]
            ))
        except mysql.connector.Error as err:
            print(f"Error inserting record: {err}")

    # Commit the transaction
    db_connection.commit()

except mysql.connector.Error as err:
    print(f"Database connection error: {err}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()

print(f"{num_records} records attempted to insert into Employees table.")

### INSERTING DATA INTO MANAGER TABLE :

def generate_random_manager(employee_ids):
    return {
        "Manager_ID": fake.unique.random_number(digits=5),
        "Manager_name": fake.name(),
        "Employee_ID": random.choice(employee_ids),
        "Assigned_date": fake.date_between(start_date='-5y', end_date='today')
    }

# Connect to the MySQL database

try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nineleaps",
        database="employee_management_system_schema"
    )

    cursor = db_connection.cursor()

    # Fetch existing Employee_IDs to use in Manager table
    cursor.execute("SELECT Employee_ID FROM employee_data;")
    employee_ids = [row[0] for row in cursor.fetchall()]

    # Generate and insert random data into Manager table
    num_records = 100  # Number of records to insert

    for _ in range(num_records):
        manager = generate_random_manager(employee_ids)
        insert_query = """
        INSERT INTO manager_details (
            Manager_ID, Manager_name, Employee_ID, Assigned_date
        ) VALUES (%s, %s, %s, %s);
        """
        try:
            cursor.execute(insert_query, (
                manager["Manager_ID"], manager["Manager_name"], manager["Employee_ID"], manager["Assigned_date"]
            ))
        except mysql.connector.Error as err:
            print(f"Error inserting record into Manager table: {err}")

    # Commit the transaction
    db_connection.commit()

except mysql.connector.Error as err:
    print(f"Database connection error: {err}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()

print(f"{num_records} records attempted to insert into Manager table.")

#### INSERTING INTO PROJECT ASSIGNMENT TABLE :

def generate_random_project_assignment(employee_ids, project_ids):
    return {
        "Project_ID": random.choice(project_ids),
        "Project_name": fake.word(),
        "Project_description": fake.sentence(),
        "Project_start_date": fake.date_between(start_date='-2y', end_date='today'),
        "Project_end_date": fake.date_between(start_date='today', end_date='+1y'),
        "Employee_ID": random.choice(employee_ids),
        "Project_assigned_date": fake.date_between(start_date='-2y', end_date='today')
    }

# Connect to the MySQL database
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nineleaps",
        database="employee_management_system_schema"
    )

    cursor = db_connection.cursor()

    # Fetch existing Employee_IDs and Project_IDs from Employee_data
    cursor.execute("SELECT Employee_ID FROM employee_data;")
    employee_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT Project_ID FROM employee_data;")
    project_ids = [row[0] for row in cursor.fetchall()]

    # Generate and insert random data into Project_assigned_details table
    num_records = 100  # Number of records to insert
    inserted_count = 0  # Counter for successfully inserted records

    for _ in range(num_records):
        project_assignment = generate_random_project_assignment(employee_ids, project_ids)
        check_query = """
        SELECT COUNT(*) FROM project_assigned_details
        WHERE Project_ID = %s AND Employee_ID = %s;
        """
        cursor.execute(check_query, (project_assignment["Project_ID"], project_assignment["Employee_ID"]))
        if cursor.fetchone()[0] == 0:  # No duplicate found
            insert_query = """
            INSERT INTO project_assigned_details (
                Project_ID, Project_name, Project_description, Project_start_date, Project_end_date,
                Employee_ID, Project_assigned_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            try:
                cursor.execute(insert_query, (
                    project_assignment["Project_ID"], project_assignment["Project_name"], project_assignment["Project_description"],
                    project_assignment["Project_start_date"], project_assignment["Project_end_date"],
                    project_assignment["Employee_ID"], project_assignment["Project_assigned_date"]
                ))
                inserted_count += 1
            except mysql.connector.Error as err:
                print(f"Error inserting record into Project_assigned_details table: {err}")
        else:
            print(f"Duplicate found for Project_ID {project_assignment['Project_ID']} and Employee_ID {project_assignment['Employee_ID']}, skipping insertion.")

    # Commit the transaction
    db_connection.commit()

except mysql.connector.Error as err:
    print(f"Database connection error: {err}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()

print(f"{inserted_count} records successfully inserted into Project_assigned_details table out of {num_records} attempts.")