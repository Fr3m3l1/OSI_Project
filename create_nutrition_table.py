import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('nutrition_data.db')
cursor = conn.cursor()

# Create the table product
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_data (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT UNIQUE,
        product_name TEXT,
        calories REAL,
        protein REAL,
        carbs REAL,
        fats REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create the table user
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        password TEXT, 
    )
''')

# Creat the table Consumed
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS cosumed_data (
        cosumed_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_id INTEGER PRIMARY KEY AUTOINCREMENT,
	amout REAL, 
	consume_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    )
''') 

# Creat the table weekly stats

# Commit changes and close the connection
conn.commit()
conn.close()

print("Table created successfully.")
