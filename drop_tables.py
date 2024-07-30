from connection import conn

cursor = conn.cursor()

### DROPPING Employee Details table 
employee_query = """
DROP TABLE employee_data
"""

### DROPPING Manager details table
manager_details_query = """
DROP TABLE manager_details
"""

### DROPPING Project assigned table 
project_assigned_query = """
DROP TABLE project_assigned_details
"""

### QUERY execution :
cursor.execute(employee_query)
cursor.execute(manager_details_query)
cursor.execute(project_assigned_query)

print("Tables dropped successfully")