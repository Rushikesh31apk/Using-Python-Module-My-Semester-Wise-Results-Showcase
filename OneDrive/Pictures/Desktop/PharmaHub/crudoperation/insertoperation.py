import sqlite3
import uuid
from datetime import date
from flask import jsonify

# Function to insert a new user into the Users table
def createUser(name, password, phone_number, email, address, pinCode):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    user_id = str(uuid.uuid4())  # Generate a unique user_id
    date_of_account_creation = date.today()

    cursor.execute('''
        INSERT INTO Users (user_id, password, level, date_of_account_creation, isApproved, block, name, email, phone_number, pinCode, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, password, 1, date_of_account_creation, 0, 0, name, email, phone_number, pinCode, address))

    conn.commit()
    conn.close()

    return {"user_id": user_id, "name": name, "email": email}   


# Function to add a new product to the database
def add_product(name, price, category, stock, certified):

    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    product_id = str(uuid.uuid4())  # Generate a unique product_id

    # Insert new product into the Products table
    cursor.execute('''
    INSERT INTO Products (product_id, product_name, stock, price, category, certified)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (product_id, name, stock, price, category, certified))

    conn.commit()
    conn.close()


    # Function to add a new order to the database


# Function to add a new order to the database
def add_order_details(product_id, user_id, product_name, user_name, total_amount, quantity, price, category, message=""):
    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        # Generate a unique order ID
        order_id = str(uuid.uuid4())

        # Get the current date and time
        order_date = date.today()

        # Insert order details into the database
        cursor.execute('''
            INSERT INTO Orders (order_id, product_id, user_id, product_name, user_name, total_amount, quantity, message, price, category, date_of_order_creation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, product_id, user_id, product_name, user_name, total_amount, quantity, message, price, category, order_date))

        conn.commit()  # Commit the transaction to save changes
        conn.close()   # Close the database connection

        return order_id  # Return the order ID of the newly created order
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Log the database error
        raise  # Re-raise the exception so it can be caught in the route handler
    except Exception as e:
        print(f"Error: {e}")  # Log other errors
        raise  # Re-raise the exception to handle it at the route level


# Function to create a new sell history record
def create_sell_history(product_id, quantity, remaining_stock, total_amount, price, product_name, user_name, user_id):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Generate a unique sell history ID
    sell_history_id = str(uuid.uuid4())
    
    # Get the current date and time for the sell record
    date_of_sale = date.today()

    # Insert the sell history record into the database
    cursor.execute(''' 
        INSERT INTO SellHistory (sell_history_id, product_id, quantity, remaining_stock, total_amount, price, product_name, user_name, user_id, date_of_sale)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sell_history_id, product_id, quantity, remaining_stock, total_amount, price, product_name, user_name, user_id, date_of_sale))

    conn.commit()
    conn.close()
    return sell_history_id

# Function to add a product to the UserStock table
def add_to_user_stock(product_name, category, price, stock, user_name, user_id):
    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        # Generate a unique UUID for stock_id
        stock_id = str(uuid.uuid4())

        # Insert new entry into the UserStock table
        cursor.execute('''
        INSERT INTO UserStock (stock_id, product_name, category, price, stock, user_name, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (stock_id, product_name, category, price, stock, user_name, user_id))

        conn.commit()
        
    except sqlite3.IntegrityError as e:
        # Handle database integrity errors (e.g., duplicate entries)
        return jsonify({"message": f"Integrity error: {str(e)}", "status": 400}), 400
    except sqlite3.DatabaseError as e:
        # Handle other database errors
        return jsonify({"message": f"Database error: {str(e)}", "status": 500}), 500
    except Exception as e:
        # Catch-all for any other errors
        return jsonify({"message": f"An unexpected error occurred: {str(e)}", "status": 500}), 500
    finally:
        conn.close()  # Ensure connection is closed even if an error occurs

    return jsonify({"message": "Product added to UserStock successfully", "status": 200}), 200




