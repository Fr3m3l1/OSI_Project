import sqlite3
import multiprocessing
import streamlit.web.cli as stcli
import schedule
import time
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

from data import create_nutrition_table


db_name = "nutritrack/data/nutrition_data.db"

# Load environment variables from .env file
load_dotenv()
# Check if local enviroment is set
if os.getenv("ENV") == "Local":
    local_env = True
else:
    local_env = False
    db_name = "/home/ubuntu/OSI_Project/nutritrack/data/nutrition_data.db"

# Access the SQLite database
def access_db():
    create_nutrition_table.create_table(db_name)

# Task to be run periodically (simulates a cron job)
def cron_job():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("SELECT * FROM Users WHERE username = ?", ("Fr3m3l",))
    user = cursor.fetchone()
    if user:
        print(f"[{timestamp}] - Found user with username: {user[1]}")
    else:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", ("Fr3m3l", "password"))
        print(f"[{timestamp}] - User not found.")
    conn.commit()
    conn.close()
    print(f"[{timestamp}] - cron job executed.")

# Function to schedule tasks
def schedule_cron():
    schedule.every(1).minutes.do(cron_job)  # Runs the cron job every minute
    while True:
        schedule.run_pending()
        time.sleep(1)

# Function to start the Streamlit server
def run_streamlit():
    if local_env:
        sys.argv = ["streamlit", "run", "nutritrack/web/main.py", db_name, "--server.port", "8501"]
    else:
        sys.argv = ["streamlit", "run", "nutritrack/web/main.py", db_name, "--server.port", "32223", "--server.enableCORS", "false"]
    stcli.main()

# Main function to start processes
if __name__ == "__main__":
    # Start the cron job scheduler and Streamlit server in parallel
    access_db()
    cron_process = multiprocessing.Process(target=schedule_cron)
    streamlit_process = multiprocessing.Process(target=run_streamlit)

    cron_process.start()
    streamlit_process.start()

    cron_process.join()
    streamlit_process.join()
