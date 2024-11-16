import sqlite3
import json

# Function to get all users from the database
def get_all_users():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Query to fetch all users from the Users table
    cursor.execute('''
        SELECT id, user_id, password, level, date_of_account_creation, isApproved, block, name, address, email, phone_number, pinCode FROM Users
    ''')

    users = cursor.fetchall()  # Fetch all user records
    conn.close()

    # Converting user data into a list of dictionaries
    users_list = []
    for user in users:
        user_dict = {
            "id": user[0],
            "user_id": user[1],
            "password": user[2],
            "level": user[3],
            "date_of_account_creation": user[4],
            "isApproved": user[5],
            "block": user[6],
            "name": user[7],
            "address": user[8],
            "email": user[9],
            "phone_number": user[10],
            "pinCode": user[11]
        }
        users_list.append(user_dict)

    return users_list# Function to get a specific user by user_id


def get_users_by_name(name):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Query to fetch user details based on name
    cursor.execute('''
        SELECT * FROM Users WHERE email=?
    ''', (name,))

    users = cursor.fetchall()  # Fetch all matching records
    conn.close()

    if users:
        # Convert each user record into a dictionary
        users_list = []
        for user in users:
            user_dict = {
                "id": user[0],
                "user_id": user[1],
                "password": user[2],
                "level": user[3],
                "date_of_account_creation": user[4],
                "isApproved": user[5],
                "block": user[6],
                "name": user[7],
                "address": user[8],
                "email": user[9],
                "phone_number": user[10],
                "pinCode": user[11]
            }
            users_list.append(user_dict)
        return users_list
    else:
        return None  # Return None if no users are found
    
def get_user_approval_status(email):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Query to fetch user approval status based on email
    cursor.execute('''
        SELECT isApproved FROM Users WHERE email=?
    ''', (email,))

    result = cursor.fetchone()  # Fetch the single matching record
    conn.close()

    if result:
        is_approved = result[0]
        # Check approval status and return accordingly
        return "disapproved" if not is_approved else "approved"
    else:
        return "User not found"  # Return if no user is found
    
    
# Function to fetch all products from the database
def get_all_products():
    try:
        # Establishing connection to SQLite database
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        # Query to fetch all products
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()

        # Convert query result to a list of dictionaries
        product_list = []
        for row in products:
            product = {
                "id": row[0],
                "product_id":row[1],
                "product_name": row[2],
                "price": row[3],
                "stock": row[4],
                "category": row[5],
                "certified": row[6],

            }
            product_list.append(product)

        return product_list
    except sqlite3.Error as db_error:
        raise Exception(f"Database error: {str(db_error)}")  # More specific exception handling for DB errors
    except Exception as e:
        raise Exception(f"Error fetching products: {str(e)}")
    finally:
        # Ensure the connection is closed to avoid memory leaks
        if conn:
            conn.close()

# Function to fetch products by name from the database
def get_products_by_name(name):
    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        # Use a case-insensitive search for matching product names
        cursor.execute("SELECT product_id,product_name ,stock,price ,category ,certified FROM Products WHERE product_name LIKE ?", ('%' + name + '%',))
        products = cursor.fetchall()

        product_list = []
        for row in products:
            product = {
                "id": row[0],
                "product_id":[1],
                "product_name": row[2],
                "price": row[3],
                "certified": row[4],
                "stock": row[5],
                "category": row[6],

            }
            product_list.append(product)

        conn.close()
        return product_list
    except sqlite3.Error as db_error:
        raise Exception(f"Database error: {str(db_error)}")
    except Exception as e:
        raise Exception(f"Error fetching products by name: {str(e)}")
    finally:
        if conn:
            conn.close()


# Function to fetch all orders from the database
def get_all_orders():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Query to fetch all orders
    cursor.execute('''
        SELECT id, order_id, user_id, product_id, isApproved, quantity, date_of_order_creation, price, total_amount, product_name, user_name, message, category
        FROM Orders
    ''')
    
    # Fetch all orders
    orders = cursor.fetchall()
    conn.close()

    # Convert orders to a list of dictionaries
    order_list = []
    for order in orders:
        order_dict = {
            "id": order[0],
            "order_id": order[1],
            "user_id": order[2],
            "product_id": order[3],
            "isApproved": order[4],
            "quantity": order[5],
            "date_of_order_creation": order[6],
            "price": order[7],
            "total_amount": order[8],
            "product_name": order[9],
            "user_name": order[10],
            "message": order[11],
            "category": order[12]
        }
        order_list.append(order_dict)

    return order_list


# Function to fetch order details based on filters
def get_order_details_by_filter(user_id, isApproved):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Query to fetch orders based on user_id and isApproved status
    query = """
    SELECT * FROM Orders WHERE user_id = ? AND isApproved = ?
    """
    cursor.execute(query, (user_id, isApproved))
    orders = cursor.fetchall()
    conn.close()

    # Convert fetched data into a list of dictionaries
    order_list = []
    for order in orders:
        order_dict = {
            "id": order[0],
            "order_id": order[1],
            "user_id": order[2],
            "product_id": order[3],
            "isApproved": order[4],
            "quantity": order[5],
            "date_of_order_creation": order[6],
            "price": order[7],
            "total_amount": order[8],
            "product_name": order[9],
            "user_name": order[10],
            "message": order[11],
            "category": order[12]
        }
        order_list.append(order_dict)

    return order_list


# Function to fetch sell history records from the database
def get_sell_history():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM SellHistory")
    records = cursor.fetchall()
    
    # Prepare the response data
    sell_history = []
    for record in records:
        sell_history.append({
            "id": record[0],  # Assuming the first column is the id
            "sell_id": record[1],
            "product_id": record[2],
            "quantity": record[3],
            "remaining_stock": record[4],
            "date_of_sell": record[10],  # Adjust according to your column index
            "total_amount": record[5],
            "price": record[6],
            "product_name": record[7],
            "user_name": record[8],
            "user_id": record[9]
        })
    
    conn.close()
    return sell_history


# Function to fetch sell history records for a specific user
def get_sell_history_by_user_id(user_id):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM SellHistory WHERE user_id = ?", (user_id,))
    records = cursor.fetchall()
    
    # Prepare the response data
    sell_history = []
    for record in records:
        sell_history.append({
            "id": record[0],  # Assuming the first column is the id
            "sell_id": record[1],
            "product_id": record[2],
            "quantity": record[3],
            "remaining_stock": record[4],
            "date_of_sell": record[10],  # Adjust according to your column index
            "total_amount": record[5],
            "price": record[6],
            "product_name": record[7],
            "user_name": record[8],
            "user_id": record[9]
        })
    
    conn.close()
    return sell_history


# Function to get all products from user stock
def get_user_stock_products():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM UserStock''')  # Ensure you're selecting from the correct table, UserStock
    products = cursor.fetchall()
    
    # Convert the fetched data to a list of dictionaries
    product_list = []
    for product in products:
        product_dict = {
            "id": product[0],
            "products_id": product[1],  # Assuming the second column is the product ID
            "name": product[2],
            "price": product[3],
            "category": product[4],
            "stock": product[5],
            "user_name": product[6],
            "user_id": product[7],
        }
        product_list.append(product_dict)
    
    conn.close()
    return product_list


def get_user_stock_products():

    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM UserStock''')
        products = cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        product_list = []
        for product in products:
            product_dict = {
                "id": product[0],
                "products_id": product[1],  # Assuming the second column is the product ID
                "name": product[2],
                "category": product[3],
                "price": product[4],
                "stock": product[5],
                "user_name": product[6],
                "user_id": product[7]
            }
            product_list.append(product_dict)

        conn.close()
        return product_list
    except Exception as e:
        print(f"Error: {e}")
        return []
    


    
