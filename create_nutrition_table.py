import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('nutrition_data.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT UNIQUE,
        product_name TEXT,
        calories REAL,
        protein REAL,
        carbs REAL,
        fats REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Table created successfully.")
