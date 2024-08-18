import mysql.connector
import csv

# Connect to the database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mypassword123',
    database='mydatabase'
)

# Create a cursor object using the cursor() method
cursor = connection.cursor()

# Drop the table if it exists
cursor.execute("DROP TABLE IF EXISTS new_dynamic_table;")

# Open the CSV file and read its contents
csv_file_path = 'train.csv'

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)

    # Read the header row
    headers = next(csv_reader)

    # Print the headers
    print(f'The headers in the CSV file are: {", ".join(headers)}')


    # Dynamically create the table with appropriate columns
    create_table_query = f"CREATE TABLE new_dynamic_table ({', '.join([f'{header} VARCHAR(255)' for header in headers])});"
    cursor.execute(create_table_query)

   
    # Define the SQL query for inserting data, using placeholders
    insert_query = f"INSERT INTO new_dynamic_table ({', '.join(headers)}) VALUES ({', '.join(['%s'] * len(headers))});"

    # Insert each row into the new_dynamic_table
    for row in csv_reader:
        cursor.execute(insert_query, row)

# Commit the changes
connection.commit()

# Count the number of rows in the table
cursor.execute('SELECT COUNT(*) FROM new_dynamic_table;')
result = cursor.fetchone()
print(f'The number of rows in the table is: {result[0]}')

# Close the cursor and the connection
cursor.close()
connection.close()
