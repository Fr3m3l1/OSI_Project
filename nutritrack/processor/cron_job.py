import sqlite3
from datetime import datetime, timedelta
import os
import logging

def cron_job_weekly_stats(db_name):
    try:
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
                
                logging.info(f"Weekly stats added for user_id {user_id}")
            else:
                logging.warning(f"No consumption data for user_id {user_id} in the past week")

        conn.commit()
        conn.close()
        logging.info(f"Weekly stats calculation completed.")
    except Exception as e:
        logging.error(f"An error occurred during Weekly stats creation: {e}")

def cron_job_backup_meltano(db_name):
    # Function to backup the SQLite database to a Meltano-compatible format (CSV)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    if os.getenv("ENV") == "Local":
        path = "nutritrack/data/"
    else:
        path = "data/"

    # Fetch all tables from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Write the data to a CSV file or create a new one if it doesn't exist

        with open(f"{path}/{table_name}.csv", "w") as file:
            # Write the column names
            file.write(",".join([description[0] for description in cursor.description]) + "\n")
            # Write the data rows
            for row in rows:
                file.write(",".join([str(value) for value in row]) + "\n")

        logging.info(f"CSV export created for table: {table_name}")