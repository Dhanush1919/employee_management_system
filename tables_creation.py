from connection import conn

cursor = conn.cursor()

### CREATING EMPLOYEE TABLE  : 
create_employee_query = """
CREATE TABLE employee_data (
    Employee_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Age INT,
    Address VARCHAR(255),
    Mobile_number VARCHAR(50),
    Gender VARCHAR(10),
    Education_details VARCHAR(255),
    Doj DATE,
    Department VARCHAR(100),
    Position VARCHAR(100),
    Project_ID INT,
    Project_name VARCHAR(100),
    Project_assigned_date DATE,
    Manager_ID INT,
    Tech_stack VARCHAR(255),
    Employees_known_tech_stack VARCHAR(255),
    Employee_salary DECIMAL(10, 2)
);
"""

cursor.execute(create_employee_query)
print("Table 'Employee_data' created successfully.")

### CREATING MANAGER TABLE : 
create_manager_query = """
CREATE TABLE manager_details (
    Manager_ID INT,
    Manager_name VARCHAR(100) NOT NULL,
    Employee_ID INT,
    Assigned_date DATE,
    PRIMARY KEY (Manager_ID, Employee_ID)
);
"""

cursor.execute(create_manager_query)

print("Table 'manager_details' created successfully.")

### CREATING PROJECTS ASSIGNED TABLE : 

create_projects_assigned_table_query = """
CREATE TABLE project_assigned_details (
    Project_ID INT,
    Project_name VARCHAR(100) NOT NULL,
    Project_description TEXT,
    Project_start_date DATE,
    Project_end_date DATE,
    Employee_ID INT,
    Project_assigned_date DATE,
    PRIMARY KEY (Project_ID, Employee_ID)
);
"""

# Execute the query
cursor.execute(create_projects_assigned_table_query)

# Close the cursor and connection
cursor.close()

print("Table 'project_assigned_details' created successfully.")
