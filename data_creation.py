import pandas as pd
import random
from faker import Faker

fake = Faker()

departments = ['Engineering', 'Management', 'Finance', 'Sales', 'Board of Directors']
positions = ['Trainee', 'Associate', 'Senior', 'Lead', 'Staff', 'Principal']

# Generate sample data
data = {
    'name': [fake.name() for _ in range(100)],
    'age': [random.randint(22, 60) for _ in range(100)],
    'address': [fake.address() for _ in range(100)],
    'mobile_number': [fake.phone_number() for _ in range(100)],
    'gender': [random.choice(['Male', 'Female']) for _ in range(100)],
    'education_details': [random.choice(['BSc Computer Science', 'MBA', 'BA Economics', 'PhD Physics', 'MSc Mathematics', 
                          'BBA', 'MA History', 'BSc Chemistry', 'BCom', 'MSc Biology']) for _ in range(100)],
    'doj': [fake.date_between(start_date='-20y', end_date='today').strftime('%Y-%m-%d') for _ in range(100)],
    'department': [random.choice(departments) for _ in range(100)],
    'position': [random.choice(positions) for _ in range(100)]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)

