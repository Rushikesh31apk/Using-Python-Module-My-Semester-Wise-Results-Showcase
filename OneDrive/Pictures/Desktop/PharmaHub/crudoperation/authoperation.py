import sqlite3
from flask import json


# Function to authenticate the user
def authenticate_user(email, password):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Query to check if the user exists with the provided email and password
    cursor.execute('''
        SELECT name FROM Users WHERE email=? AND password=?
    ''', (email, password))

    user = cursor.fetchone()  # Fetch the user if it exists
    conn.close()

    if user:
        return user[0]  # Return the user_id if authentication is successful
    else:
        return None  # Return None if authentication fails
   

# Function to validate admin credentials
def validate_admin_credentials(username, password):
    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        # Query to find the admin with the given username and password
        cursor.execute('''
            SELECT * FROM Admins WHERE username = ? AND password = ?
        ''', (username, password))
        
        admin = cursor.fetchone()
        conn.close()

        # Returns True if the admin exists, False otherwise
        return admin is not None

    except Exception as e:
        print(f"Error: {e}")
        return False
