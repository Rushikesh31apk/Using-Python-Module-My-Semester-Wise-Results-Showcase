import sqlite3

# Function to create the Users table
def createTableUsers():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id varchar(255),
        password TEXT NOT NULL,
        level INTEGER NOT NULL DEFAULT 1,  -- Default user level 1 (e.g., normal user)
        date_of_account_creation DATE NOT NULL,
        isApproved INTEGER NOT NULL DEFAULT 0,  -- 0 = Not approved, 1 = Approved
        block INTEGER NOT NULL DEFAULT 0,  -- 0 = Not blocked, 1 = Blocked
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone_number TEXT NOT NULL,
        pinCode varchar(25),
        address varchar(255)
    );
    ''')

    conn.commit()
    conn.close()


# Function to create the Products table
def create_table_products():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT NOT NULL,
        product_name TEXT NOT NULL,
        stock INTEGER NOT NULL,
        price INTEGER NOT NULL,
        category TEXT NOT NULL,
        certified INTEGER NOT NULL DEFAULT 0
    );
    ''')

    conn.commit()
    conn.close()


# Function to create the Orders table
def create_orders_table():
    try:
        conn = sqlite3.connect("my_medicalshop.db")  # Connect to the SQLite database
        cursor = conn.cursor()  # Create a cursor object to execute SQL queries

        # SQL query to create the Orders table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            isApproved INTEGER NOT NULL DEFAULT 0,
            quantity INTEGER NOT NULL,
            date_of_order_creation TEXT NOT NULL,
            price REAL NOT NULL,
            total_amount REAL NOT NULL,
            product_name TEXT NOT NULL,
            user_name TEXT NOT NULL,
            message TEXT,
            category TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
            );''')

        conn.commit()  # Commit the transaction to save changes
        conn.close()   # Close the database connection
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")



# Function to create the Sell History table with foreign key relationships
def create_sell_history_table():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SellHistory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sell_history_id TEXT NOT NULL UNIQUE,
        product_id TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        remaining_stock INTEGER NOT NULL,
        total_amount REAL NOT NULL,
        price REAL NOT NULL,
        product_name TEXT NOT NULL,
        user_name TEXT NOT NULL,
        user_id TEXT NOT NULL,
        date_of_sale DATETIME NOT NULL,
        FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,   -- Link to Products table
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE               -- Link to Users table
    );
    ''')
    
    conn.commit()
    conn.close()



# Function to create the UserStock table
def create_user_stock_table():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserStock(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_id TEXT NOT NULL UNIQUE,                 -- UUID for unique stock identifier
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        price INTEGER NOT NULL,
        stock INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        user_id TEXT NOT NULL
    );
    ''')

    conn.commit()
    conn.close()



# Function to create the Admins table
def create_admin_table():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()