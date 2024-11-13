import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('nutrition_data.db')
cursor = conn.cursor()

# Create the table product
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product (
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
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        password TEXT
    )
''')

# Create the table Konsumiert (Consumed)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Konsumiert (
        konsum_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        amount REAL,
        consume_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User (user_id),
        FOREIGN KEY (product_id) REFERENCES Product (product_id)
    )
''')

# Create the table Weekly Stats
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Weekly_Stats (
        weekly_stats_id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_id INTEGER,
        year INTEGER,
        user_id INTEGER,
        week_start_date DATE,
        total_calories REAL,
        total_protein REAL,
        total_carbs REAL,
        total_fats REAL,
        FOREIGN KEY (user_id) REFERENCES User (user_id)
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Tables created successfully.")
