import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Amir@12345'
    )
    cursor = connection.cursor()
    cursor.execute('USE inventory_management_system')
    cursor.execute('SELECT COUNT(*) FROM employee_data')
    count = cursor.fetchone()[0]
    print(f"Employee count: {count}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if connection:
        connection.close()
