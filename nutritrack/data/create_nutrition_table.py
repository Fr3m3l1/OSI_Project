import sqlite3
import logging

def create_table(db_name):

    logging.info(f"Connecting or creating database: {db_name}")

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Product table
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

    # User table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    # Konsumiert (Consumed) table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Konsumiert (
            konsum_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            amount REAL,
            consume_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users (user_id),
            FOREIGN KEY (product_id) REFERENCES Product (product_id)
        )
    ''')

    #Weekly Stats table
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
            FOREIGN KEY (user_id) REFERENCES Users (user_id),
            UNIQUE (week_id, year, user_id) -- Enforce unique combination
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    logging.info("Tables created successfully.")

if __name__ == "__main__":
    create_table('nutrition_data.db')
