import sqlite3

# Function to delete all users from the database
def delete_all_users():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Query to delete all users
    cursor.execute("DELETE FROM Users")
    conn.commit()
    conn.close()

    return cursor.rowcount  # Return the number of deleted rows


# Function to delete a specific user by id
def delete_specific_user(id):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Query to delete a specific user by id
    cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return cursor.rowcount  # Return the number of deleted rows


# Function to delete all products from the Products table
def delete_all_products():
    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        # Execute delete query to remove all records
        cursor.execute("DELETE FROM Products")
        conn.commit()

        # Get the number of rows deleted
        deleted_rows = cursor.rowcount
        conn.close()

        return deleted_rows
    except sqlite3.Error as db_error:
        raise Exception(f"Database error: {str(db_error)}")
    except Exception as e:
        raise Exception(f"Error deleting all products: {str(e)}")
    finally:
        if conn:
            conn.close()

# Function to delete a specific product by id
def delete_product_by_id(product_id):
    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        # Execute delete query to remove product by id
        cursor.execute("DELETE FROM Products WHERE id = ?", (product_id,))
        conn.commit()

        # Get the number of rows deleted
        deleted_rows = cursor.rowcount
        conn.close()

        return deleted_rows
    except sqlite3.Error as db_error:
        raise Exception(f"Database error: {str(db_error)}")
    except Exception as e:
        raise Exception(f"Error deleting product with ID {product_id}: {str(e)}")
    finally:
        if conn:
            conn.close()
