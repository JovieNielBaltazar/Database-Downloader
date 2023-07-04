import mysql.connector
import csv
from datetime import datetime

# Connection details
host = 'localhost'
user = 'root'
password = ''
database = 'db1'
port = 3306

# Connect to the MySQL database
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Get table names
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

# List to store table information
table_info = []

# Retrieve table names and fields
for table in tables:
    table_name = table[0]

    # Get column names for each table
    cursor.execute(f"SHOW COLUMNS FROM {table_name};")
    columns = cursor.fetchall()

    # Extract field names
    fields = [column[0] for column in columns]

    # Create dictionary for table information
    table_info.append({"table_name": table_name, "fields": ", ".join(fields)})

# Generate timestamp for file name
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Specify the file path to save the CSV data
file_path = f'D:/pythonProject/compilation of fields/compilation_of_fields_{timestamp}.csv'

# Save the table information as CSV
with open(file_path, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["table_name", "fields"])
    writer.writeheader()
    writer.writerows(table_info)

# Close the cursor and connection
cursor.close()
connection.close()


print("Download Success!")