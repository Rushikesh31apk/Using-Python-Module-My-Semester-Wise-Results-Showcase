import sqlite3


# Function to update user details
def update_user_details(id, **kwargs):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Build the SQL query dynamically based on provided fields
    query = "UPDATE Users SET "
    query += ", ".join(f"{key} = ?" for key in kwargs.keys())  # Add fields to update
    query += " WHERE id = ?"
    
    values = list(kwargs.values()) + [id]  # Gather values for the query

    cursor.execute(query, values)  # Execute the update query
    conn.commit()
    conn.close()

    return cursor.rowcount  # Return the number of updated rows


# Function to update the product in the database using **kwargs
def update_product(id, **kwargs):
    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        # Build the update query dynamically based on the provided keyword arguments
        query = "UPDATE Products SET "
        params = []
        for key, value in kwargs.items():
            query += f"{key} = ?, "
            params.append(value)

        # Remove the trailing comma and space from the query
        query = query.rstrip(', ')

        # Add the condition for updating based on id
        query += " WHERE id = ?"
        params.append(id)

        # Execute the update query
        cursor.execute(query, tuple(params))
        conn.commit()

        # Get the number of rows updated
        updated_rows = cursor.rowcount
        conn.close()

        return updated_rows
    except sqlite3.Error as db_error:
        raise Exception(f"Database error: {str(db_error)}")
    except Exception as e:
        raise Exception(f"Error updating product: {str(e)}")
    finally:
        if conn:
            conn.close()


# Function to update order details in the database
def update_order(order_id, updates):
    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        # Build the update query dynamically based on provided fields
        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [order_id]

        # Query to update the order
        query = f"UPDATE Orders SET {set_clause} WHERE order_id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return True  # Successfully updated the order

    except sqlite3.DatabaseError as e:
        # Catch database-related errors
        conn.close()  # Ensure the connection is closed
        return {"error": "Database error", "message": str(e)}

    except Exception as e:
        # Catch any other unforeseen errors
        return {"error": "Unknown error", "message": str(e)}
    


    

