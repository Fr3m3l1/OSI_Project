import sqlite3
from web.helper.miscellaneous import hash_password

# Database functions
def add_user(username, password, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # Check if user already exists
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return False
    cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", 
                   (username, hash_password(password)))
    conn.commit()
    conn.close()
    return True

def login_user(username, password, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[2] == hash_password(password):  # user[2] is the password column
        return user
    return None


def get_user_data_weekConsumed(user_id_value, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.product_name, p.calories, p.protein, p.carbs, p.fats, k.amount, k.consume_date
        FROM Konsumiert k
        JOIN Product p ON k.product_id = p.product_id
        WHERE k.consume_date >= datetime('now', '-7 days')
        AND k.user_id = ?
    ''', (user_id_value,))
    user_data = cursor.fetchall()
    conn.close()
    return user_data


def get_user_weekly_stats(user_id_value, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT week_start, calories, protein, carbs, fats
        FROM WeeklyStats
        WHERE user_id = ?
        ORDER BY week_start DESC
        LIMIT 1
    ''', (user_id_value,))
    user_stats = cursor.fetchone()
    conn.close()
    return user_stats
