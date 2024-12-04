import sqlite3
from datetime import datetime, timedelta


def cron_job(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Calculate the start and end dates of the past week (Sunday to Saturday)
    today = datetime.now()
    last_sunday = today - timedelta(days=today.weekday() + 1)
    last_sunday = last_sunday.replace(hour=23, minute=59, second=59)
    week_start = last_sunday - timedelta(days=6)
    week_id = int(week_start.strftime('%U'))  # Week number in the calendar year

    # Fetch all users from the Users table
    cursor.execute("SELECT user_id FROM Users")
    users = cursor.fetchall()
    
    for user in users:
        user_id = user[0]
        
        # Aggregate values for the past week from the Konsumiert table
        cursor.execute('''
            SELECT 
                SUM(p.calories * k.amount) AS total_calories,
                SUM(p.protein * k.amount) AS total_protein,
                SUM(p.carbs * k.amount) AS total_carbs,
                SUM(p.fats * k.amount) AS total_fats
            FROM Konsumiert k
            JOIN Product p ON k.product_id = p.product_id
            WHERE k.user_id = ? 
              AND k.consume_date BETWEEN ? AND ?
        ''', (user_id, week_start, last_sunday))
        
        stats = cursor.fetchone()
        if stats:
            total_calories, total_protein, total_carbs, total_fats = stats
            
            # Insert the weekly summary into the Weekly_Stats table
            cursor.execute('''
                INSERT INTO Weekly_Stats (
                    week_id, year, user_id, week_start_date, 
                    total_calories, total_protein, total_carbs, total_fats
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (week_id, week_start.year, user_id, week_start.date(), 
                  total_calories, total_protein, total_carbs, total_fats))
            
            print(f"[{datetime.now()}] - Weekly stats added for user_id {user_id}")
        else:
            print(f"[{datetime.now()}] - No consumption data for user_id {user_id} in the past week")

    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] - cron job executed.")

