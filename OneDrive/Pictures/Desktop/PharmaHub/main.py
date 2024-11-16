import sqlite3
from flask import Flask, jsonify, request
from crudoperation.createoperation import create_admin_table,create_orders_table,create_sell_history_table,create_table_products,create_user_stock_table,createTableUsers
from crudoperation.authoperation import authenticate_user,validate_admin_credentials
from crudoperation.insertoperation import add_order_details,add_product,add_to_user_stock,create_sell_history,createUser
from crudoperation.readoperation import get_all_orders,get_all_products,get_all_users,get_order_details_by_filter,get_products_by_name,get_sell_history,get_sell_history_by_user_id, get_user_approval_status,get_user_stock_products,get_users_by_name
from crudoperation.updateoperation import update_order,update_product,update_user_details
from crudoperation.deleteoperation import delete_all_products,delete_all_users,delete_product_by_id,delete_specific_user


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
    return "Hello <br> Rushikesh"

# API route for user signup
@app.route('/signUp', methods=['POST'])
def signup():
    try:
        # Getting data from the form request
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone_number = request.form['phone_number']
        address = request.form['address']
        pinCode = request.form['pinCode']
        
        # Create user and get the user_id
        user_details = createUser(name=name, password=password, phone_number=phone_number, email=email, address=address, pinCode=pinCode)

        # Returning success response
        return jsonify({"message": "User created successfully", "user_details": user_details}), 201

    except Exception as e:

        return jsonify({"error": str(e)}), 400
    
# API route for login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Getting data from the form request
        email = request.form['email']
        password = request.form['password']

        # Authenticate the user
        name = authenticate_user(email=email, password=password)

        if name:
            # If authentication is successful, return the user_id
            return jsonify({"message": name, "status": 200}), 200
        else:
            # If authentication fails, return an error message
            return jsonify({"message": "Invalid email or password", "status": 401}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

# API route to get all users
@app.route('/getAllUsers', methods=['GET'])
def get_all_users_route():
    try:
        # Fetch all users
        users = get_all_users()

        # Return the list of users as a JSON response
        return jsonify(users), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# API route to get all users with the same name
@app.route('/getUsersByMail', methods=['POST'])
def get_users_by_name_route():
    try:
        # Getting the name from the request
        name = request.form['email']

        # Fetch all users with the specified name
        users = get_users_by_name(name=name)

        if users:
            # If users are found, return their details
            return jsonify(users), 200
        else:
            # If no users are found, return an error message
            return jsonify({"message": "No users found with this name"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Route to check if the user is disapproved
@app.route('/check_disapproval', methods=['GET', 'POST'])
def check_disapproval():
    email = request.form['email']
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    status = get_user_approval_status(email)
    
    if status == "User not found":
        return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"status": status}), 200

# API route to update user details
@app.route('/updateUserAllDetails', methods=['PATCH'])
def update_user_all_details_route():
    try:
        # Getting user_id from the request
        id = request.form['id']

        # Getting other fields from the request
        update_fields = {key: value for key, value in request.form.items() if key != 'id'}

        if update_fields:
            # Update user details in the database
            updated_rows = update_user_details(id=id, **update_fields)

            if updated_rows > 0:
                return jsonify({'message': 'User Updated Successfully', 'status': 200}), 200
            else:
                return jsonify({'message': 'User not found or no changes made', 'status': 404}), 404
        else:
            return jsonify({'message': 'No fields to update', 'status': 400}), 400

    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500  # Include status code in case of error400


# API route to delete all users
@app.route('/deleteAllUsers', methods=['DELETE'])
def delete_all_users_route():
    try:
        # Delete all users from the database
        deleted_rows = delete_all_users()

        if deleted_rows > 0:
            return jsonify({'message': 'All Users Deleted Successfully', 'status': 200}), 200
        else:
            return jsonify({'message': 'No users found to delete', 'status': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# API route to delete a specific user
@app.route('/deleteSpecificUser', methods=['DELETE'])
def delete_specific_user_route():
    try:
        # Getting id from the request
        id = request.form('id')

        if not id:
            return jsonify({'message': 'id is required', 'status': 400}), 400

        # Delete the specific user from the database
        deleted_rows = delete_specific_user(id=id)

        if deleted_rows > 0:
            return jsonify({'message': 'User Deleted Successfully', 'status': 200}), 200
        else:
            return jsonify({'message': 'User not found', 'status': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500  # Include status code in case of error



# API route to add a new product
@app.route('/addProducts', methods=['POST'])
def add_product_route():
    try:
        # Access each field explicitly to validate its existence and data type
        name = request.form['product_name']
        category = request.form['category']
        certified = request.form.get('certified', 0)  # Default to 0 if not provided

        # Validate and convert stock and price
        try:
            price = float(request.form['price'])  # Convert price to float
            stock = int(request.form['stock'])    # Convert stock to integer
            certified = int(certified)            # Convert certified to integer (0 or 1)
        except ValueError:
            return jsonify({
                'message': 'Invalid data types. Ensure price is a number, stock is an integer, and certified is 0 or 1.',
                'status': 400
            }), 400

        # Add the product to the database
        add_product(name, price, category, stock, certified)

        return jsonify({'message': 'Product Added Successfully', 'status': 200}), 200

    except KeyError as e:
        # Handle missing fields in the form data
        return jsonify({'error': f'Missing field: {str(e)}', 'status': 400}), 400
    except Exception as e:
        return jsonify({'error': str(e), 'status': 400}), 400
    
# API route to get all products
@app.route('/getAllProducts', methods=['GET'])
def get_all_products_route():
    try:
        products = get_all_products()
        return jsonify({'products': products, 'status': 200}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 400}), 400  # Return error details in case of failure
    

# API route to get products by name
@app.route('/getProductsByName', methods=['POST'])
def get_products_by_name_route():
    try:
        # Get the product_name from the form data
        product_name = request.form.get('product_name')

        if not product_name:
            return jsonify({'message': 'Product name is required', 'status': 400}), 400

        products = get_products_by_name(product_name)
        if products:
            return jsonify({'products': products, 'status': 200}), 200
        else:
            return jsonify({'message': 'No products found matching the name', 'status': 404}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'status': 400}), 400

    

# API route to update a product
@app.route('/updateProduct', methods=['PATCH'])
def update_product_route():
    try:
        # Get the product ID from query parameters
        id = request.form['id']

        # Ensure that id is provided
        if not id:
            return jsonify({'message': 'Product ID (id) is required', 'status': 400}), 400

        # Get optional fields from form data
        updated_fields = {key: request.form.get(key) for key in ['name', 'price', 'category', 'stock'] if request.form.get(key)}

        if not updated_fields:
            return jsonify({'message': 'At least one field to update is required', 'status': 400}), 400

        # Update the product details with provided values
        updated_rows = update_product(id, **updated_fields)

        if updated_rows > 0:
            return jsonify({'message': 'Product updated successfully', 'status': 200}), 200
        else:
            return jsonify({'message': 'Product not found or no changes made', 'status': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500
    
    

@app.route('/deleteAllProducts', methods=['DELETE'])
def delete_all_products_route():
    try:
        # Call the function to delete all products
        deleted_rows = delete_all_products()

        if deleted_rows > 0:
            return jsonify({'message': 'All products deleted successfully', 'status': 200}), 200
        else:
            return jsonify({'message': 'No products to delete', 'status': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500
    

@app.route('/deleteProductByid', methods=['DELETE'])
def delete_product_by_name_route():
    try:
        # Get the product name from the request JSON
        product_id= request.form['id']

        if not product_id:
            return jsonify({'message': 'Product name is required', 'status': 400}), 400

        # Call the function to delete the product by name
        deleted_rows = delete_product_by_id(product_id)

        if deleted_rows > 0:
            return jsonify({'message': f'Product "{product_id}" deleted successfully', 'status': 200}), 200
        else:
            return jsonify({'message': f'Product "{product_id}" not found', 'status': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status': 500}), 500

@app.route('/addOrderDetails', methods=['POST'])
def add_order_details_route():
    try:
        # Getting parameters from the request
        product_id = request.form['product_id']
        user_id = request.form['user_id']
        product_name = request.form['product_name']
        user_name = request.form['user_name']

        # Convert values to the appropriate types and handle missing fields
        total_amount = float(request.form['total_amount'])  # Convert to float
        quantity = int(request.form['quantity'])  # Convert to int
        message = request.form.get('message', '')  # Optional field (default to empty string)
        price = float(request.form['price'])  # Convert to float
        category = request.form['category']

        # Add the order to the database by calling the updated function
        order_id = add_order_details(product_id, user_id, product_name, user_name, total_amount, quantity, price, category, message)

        if order_id:
            return jsonify({'message': 'Order Created Successfully', 'status': 200, 'order_id': order_id}), 200
        else:
            return jsonify({'message': 'Error creating order', 'status': 500}), 500

    except KeyError as ke:
        # Handling missing required fields
        print(f"Missing key: {ke}")
        return jsonify({'error': f'Missing required field: {str(ke)}'}), 400
    except ValueError as ve:
        # Handling invalid data type (e.g., non-numeric values for amount or quantity)
        print(f"Value error: {ve}")
        return jsonify({'error': f'Invalid data type: {str(ve)}'}), 400
    except sqlite3.Error as e:
        # Handling database errors
        print(f"Database error: {e}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        # Catching any other unforeseen errors
        print(f"General error: {e}")
        return jsonify({'error': f'Error: {str(e)}'}), 500


# API route to get all order details
@app.route('/getAllOrdersDetail', methods=['GET'])
def get_all_orders_route():
    try:
        orders = get_all_orders()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API route to get order details by filter
@app.route('/getOrderDetailsByFilter', methods=['POST'])
def get_order_details_route():
    # Retrieve user_id and isApproved from the form data using request.form[]
    try:
        user_id = request.form['user_id']  # Retrieve user_id from form
        isApproved = request.form['isApproved']  # Retrieve approval status from form

        # Fetch order details using the filter
        orders = get_order_details_by_filter(user_id, isApproved)
        return jsonify(orders), 200
    except KeyError as ke:
        return jsonify({'error': f'Missing required field: {str(ke)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500
  

@app.route('/updateOrderDetails', methods=['PATCH'])
def update_order_route():
    order_id = request.form['order_id']  # Retrieve order_id from form data
    if not order_id:
        return jsonify({'message': 'Order ID is required', 'status': 400}), 400

    # Retrieve other fields from form data
    updates = {k: v for k, v in request.form.items() if k != 'order_id'}

    try:
        update_result = update_order(order_id, updates)
        if isinstance(update_result, dict):  # If an error occurs, return the error message
            return jsonify(update_result), 500

        return jsonify({'message': 'Order Updated Successfully', 'status': 200}), 200
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/createSellHistory', methods=['POST'])
def create_sell_history_route():
    try:
        # Retrieve form data using request.form['']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        remaining_stock = request.form['remaining_stock']
        total_amount = request.form['total_amount']
        price = request.form['price']
        product_name = request.form['product_name']
        user_name = request.form['user_name']
        user_id = request.form['user_id']

        # Check if all required fields are provided
        if not all([product_id, quantity, remaining_stock, total_amount, price, product_name, user_name, user_id]):
            return jsonify({'message': 'All fields are required', 'status': 400}), 400

        # Call the function to create the sell history
        create_sell_history(product_id, quantity, remaining_stock, total_amount, price, product_name, user_name, user_id)
        return jsonify({'message': 'Sell History Created Successfully', 'status': 200}), 200

    except KeyError as e:
        # Handle missing required form data
        return jsonify({'error': f'Missing required field: {str(e)}', 'status': 400}), 400
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e), 'status': 500}), 500


@app.route('/getSellHistory', methods=['GET'])
def get_sell_history_route():
    sell_history = get_sell_history()
    return jsonify(sell_history)

@app.route('/getSellHistoryByUserId', methods=['POST'])
def get_sell_history_by_user_id_route():
   
    user_id = request.form['user_id']
    
    if not user_id:
        return jsonify({"message": "User ID is required", "status": 400}), 400
    
    sell_history = get_sell_history_by_user_id(user_id)
    
    if not sell_history:
        return jsonify({"message": "No sell history found for this user", "status": 404}), 404
    
    return jsonify(sell_history)



# Route to add a product to the UserStock table
@app.route('/addToProductsUserStock', methods=['POST'])
def add_to_products_user_stock_route():
    try:
        product_name = request.form['product_name']
        category = request.form['category']
        price = int(request.form['price'])
        stock = int(request.form['stock'])
        user_name = request.form['user_name']   
        user_id = request.form['user_id']
        
        # Add to user stock
        add_to_user_stock(product_name, category, price, stock, user_name, user_id)
        
        return jsonify({"message": "Add To Products Successfully", "status": 200}), 200
    except KeyError as e:
        return jsonify({"message": f"{e.args[0]} is required", "status": 400}), 400
    except ValueError as e:
        return jsonify({"message": f"Invalid input: {str(e)}", "status": 400}), 400
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}", "status": 500}), 500



@app.route('/getProductsUserStock', methods=['GET'])
def get_products_user_stock_route():
    products = get_user_stock_products()

    if not products:
        return jsonify({"message": "No products found"}), 404
    
    return jsonify(products)


# Route to validate admin's ID and password using form data
@app.route('/validateAdmin', methods=['POST'])
def validate_admin_route():
    try:
        # Retrieving data from the form using request.form['key']
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return jsonify({"message": "Admin Username and password are required", "status": 400}), 400

        # Validate credentials
        if validate_admin_credentials(username, password):
            return jsonify({"message": "Admin validated successfully", "status": 200}), 200
        else:
            return jsonify({"message": "Invalid admin username or password", "status": 401}), 401
    
    except KeyError as e:
        # In case the required keys are missing in the form data
        return jsonify({"message": f"Missing field: {str(e)}", "status": 400}), 400

if __name__ == '__main__':
    createTableUsers()
    create_table_products()
    create_orders_table()
    create_sell_history_table()
    create_user_stock_table()
    create_admin_table()
    app.run(debug=True)