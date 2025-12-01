import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with actual username
        password="Amir@12345",  # Replace with actual password
        database="inventory_management_system",
        auth_plugin='Amir@12345'
    )
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()