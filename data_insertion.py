import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Define possible tech stacks
tech_stacks = [
    ["Business Intelligence", "Dashboard building"],
    ["Building Data Pipelines", "Performing EDA", "Data Manipulation"],
    ["Model Building", "Model deployment"],
    ["Cryptography", "Cybersecurity"],
    ["Gen AI", "Langchain", "OpenAI", "Model development"],
    ["Data Analysis", "Statistical Modeling"],
    ["Cloud Computing", "AWS", "Azure"],
    ["Machine Learning", "Deep Learning"],
    ["Data Visualization", "Tableau", "Power BI"],
    ["Software Development", "Agile Methodologies"],
    ["Blockchain", "Quantum Computing"],
    ["Funding and Investment management", "Business Management"]
]

# Function to generate random data
def generate_random_employee():
    tech_stack = ', '.join(random.choice(tech_stacks))
    return {
        "Employee_ID": fake.unique.random_number(digits=5),
        "Name": fake.name(),
        "Age": random.randint(22, 60),
        "Address": fake.address(),
        "Mobile_number": "+91" + str(fake.random_number(digits=10, fix_len=True)),
        "Gender": random.choice(["Male", "Female"]),
        "Education_details": random.choice(["BE (ECE)", "BE (MECH)", "BE (CIVIL)", "BE (CSE)","MBA (FINANCE)", "MBA (HR)", "MBA (BUSINESS MANAGEMENT)", "BTECH (ARCH)", "Bsc (Comp Sci)" ]),
        "Doj": fake.date_between(start_date='-10y', end_date='today'),
        "Department": random.choice(["HR", "Engineering", "Marketing", "Sales", "Analytics", "Product Management", "Customer Support"]),
        "Position": random.choice(["Intern", "Trainee", "Associate", "Senior Associate", "Lead", "Staff", "Principal"]),
        "Employees_known_tech_stack": tech_stack,
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
            Doj, Department, Position, Employees_known_tech_stack, Employee_salary
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            cursor.execute(insert_query, (
                employee["Employee_ID"], employee["Name"], employee["Age"], employee["Address"],
                employee["Mobile_number"], employee["Gender"], employee["Education_details"],
                employee["Doj"], employee["Department"], employee["Position"],
                employee["Employees_known_tech_stack"], employee["Employee_salary"]
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

print(f"{num_records} records attempted to insert into employee_data table.")

### INSERTING DATA INTO MANAGER TABLE :

# Initialize Faker
fake = Faker()

# Function to generate random manager data
def generate_random_manager(manager_id):
    return {
        "Manager_ID": manager_id,
        "Manager_name": fake.name()
    }

# Function to generate random manager assignment data
def generate_random_manager_assignment(manager_id, employee_id, doj):
    return {
        "Manager_ID": manager_id,
        "Employee_ID": employee_id,
        "Assigned_date": doj
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

    # Fetch existing Employee_IDs and Doj from employee_data table
    cursor.execute("SELECT Employee_ID, Doj FROM employee_data;")
    employee_data = cursor.fetchall()
    employee_ids = [row[0] for row in employee_data]
    employee_doj = {row[0]: row[1] for row in employee_data}

    # Generate 10 managers
    manager_ids = [fake.unique.random_number(digits=5) for _ in range(10)]
    managers = [generate_random_manager(manager_id) for manager_id in manager_ids]

    # Insert managers into manager_details table
    for manager in managers:
        insert_manager_query = """
        INSERT INTO manager_details (
            Manager_ID, Manager_name, Employee_ID, Assigned_date
        ) VALUES (%s, %s, %s, %s);
        """
        for employee_id in employee_ids[:10]:  # Assign first 10 employees to each manager
            try:
                cursor.execute(insert_manager_query, (
                    manager["Manager_ID"], manager["Manager_name"], employee_id, employee_doj[employee_id]
                ))
                employee_ids.remove(employee_id)
            except mysql.connector.Error as err:
                print(f"Error inserting manager record: {err}")

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

print("Records inserted into Manager table.")

#### INSERTING INTO PROJECT ASSIGNMENT TABLE :

# Initialize Faker
fake = Faker()

# Predefined list of unique projects
projects = [
    {"Project_ID": 1001, "Project_name": "Data Science & ML", "Project_description": "Developing predictive models and algorithms for data-driven insights."},
    {"Project_ID": 1002, "Project_name": "Block Chain & Quantum Computing", "Project_description": "Innovating secure transactions using blockchain and quantum computing."},
    {"Project_ID": 1003, "Project_name": "Product Management", "Project_description": "Overseeing product development and market strategy."},
    {"Project_ID": 1004, "Project_name": "Data Pipelines and ETLs", "Project_description": "Building efficient data pipelines and ETL processes for seamless data integration."},
    {"Project_ID": 1005, "Project_name": "Gen AI and Artificial Intelligence", "Project_description": "Advancing AI models for intelligent automation and decision-making."},
    {"Project_ID": 1006, "Project_name": "Quantum computing", "Project_description": "Exploring the potential of quantum computing for complex problem-solving."},
    {"Project_ID": 1008, "Project_name": "DEV OPS", "Project_description": "Streamlining development and operations for continuous delivery."},
    {"Project_ID": 1009, "Project_name": "DEV SEC OPS & Cyber security", "Project_description": "Enhancing security measures in DevOps environments."},
    {"Project_ID": 1010, "Project_name": "Customer engagement and Retention", "Project_description": "Strategies to boost customer engagement and retention rates."}
]

# Function to generate project assignment details
def generate_project_assignment(employee_id, project, start_date, end_date=None):
    return {
        "Project_ID": project["Project_ID"],
        "Project_name": project["Project_name"],
        "Project_description": project["Project_description"],
        "Project_start_date": start_date,
        "Project_end_date": end_date,
        "Employee_ID": employee_id,
        "Project_assigned_date": start_date
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

    # Fetch existing Employee_IDs and Doj from employee_data
    cursor.execute("SELECT Employee_ID, Doj FROM employee_data;")
    employee_data = cursor.fetchall()
    employee_ids = [row[0] for row in employee_data]
    employee_doj = {row[0]: row[1] for row in employee_data}

    # Function to insert project assignments
    def insert_project_assignments(assignments):
        insert_query = """
        INSERT INTO project_assigned_details (
            Project_ID, Project_name, Project_description, Project_start_date, Project_end_date,
            Employee_ID, Project_assigned_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        for assignment in assignments:
            try:
                cursor.execute(insert_query, (
                    assignment["Project_ID"], assignment["Project_name"], assignment["Project_description"],
                    assignment["Project_start_date"], assignment["Project_end_date"],
                    assignment["Employee_ID"], assignment["Project_assigned_date"]
                ))
            except mysql.connector.Error as err:
                print(f"Error inserting record into Project_assigned_details table: {err}")

    # Insert records for 15 employees with more than 3 projects
    employees_more_than_3_projects = employee_ids[:15]
    for employee_id in employees_more_than_3_projects:
        doj = employee_doj[employee_id]
        start_date = doj
        assignments = []
        for i in range(3):
            end_date = start_date + timedelta(days=(15 * (i+1)))
            assignments.append(generate_project_assignment(employee_id, projects[i], start_date, end_date))
            start_date = end_date + timedelta(days=1)
        # Current ongoing project
        assignments.append(generate_project_assignment(employee_id, projects[3], start_date, None))
        insert_project_assignments(assignments)

    # Insert records for 25 employees with 2 different projects
    employees_two_projects = employee_ids[15:40]
    for employee_id in employees_two_projects:
        doj = employee_doj[employee_id]
        start_date = doj
        assignments = []
        end_date = start_date + timedelta(days=30)
        assignments.append(generate_project_assignment(employee_id, projects[4], start_date, end_date))
        start_date = end_date + timedelta(days=1)
        assignments.append(generate_project_assignment(employee_id, projects[5], start_date, None))
        insert_project_assignments(assignments)

    # Insert records for 35 employees currently working on a single project
    employees_single_project = employee_ids[40:75]
    for employee_id in employees_single_project:
        doj = employee_doj[employee_id]
        start_date = doj
        assignments = [generate_project_assignment(employee_id, projects[6], start_date, None)]
        insert_project_assignments(assignments)

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

print("Records successfully inserted into Project_assigned_details table.")