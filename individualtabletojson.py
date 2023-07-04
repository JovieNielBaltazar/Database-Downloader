import json
import os
import mysql.connector
from datetime import datetime

# Connection details
host = 'localhost'
user = 'root'
password = ''
database = 'db1'
port = 3306

try:
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

    # Get a list of all tables in the database
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    # Directory path to save the JSON files
    output_dir = 'D:/pythonProject/JsonTables'
    os.makedirs(output_dir, exist_ok=True)

    # Export each table as a JSON file
    for table in tables:
        table_name = table[0]
        output_path = os.path.join(output_dir, f'{table_name}.json')

        # Retrieve all rows from the table
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        # Get the column names of the table
        cursor.execute(f"SHOW COLUMNS FROM {table_name};")
        columns = [column[0] for column in cursor.fetchall()]

        # Prepare the data to be written as JSON
        data = {
            "type": "table",
            "name": table_name,
            "database": database,
            "data": []
        }
        for row in rows:
            row_data = {}
            for i, column in enumerate(columns):
                value = row[i]
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                row_data[column] = value
            data["data"].append(row_data)

        # Write the data to a JSON file
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4, default=str)  # Use default=str to handle datetime objects

    print("Export completed successfully.")

except mysql.connector.Error as error:
    print("Error connecting to the MySQL database:", error)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
