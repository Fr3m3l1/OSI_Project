import multiprocessing
import streamlit.web.cli as stcli
import schedule
import time
import sys
import os
from dotenv import load_dotenv
from processor.cron_job import cron_job
from data import create_nutrition_table

# Environment variables from .env file
load_dotenv()

# Determine the environment (local or production) based on ENV variable
if os.getenv("ENV") == "Local":
    print("Running in local environment.")
    db_name = "nutritrack/data/nutrition_data.db"
    local_env = True
else:
    print("Running in production environment.")
    db_name = "data/nutrition_data.db"
    local_env = False

# Access the SQLite database
def access_db():
    create_nutrition_table.create_table(db_name)

# Function to schedule tasks and run jobs
def schedule_cron(db_name):
    # Different tasks schedul based on environment
    if local_env:
        # Local environment: Cron job runs every 1 minute
        schedule.every(1).minutes.do(cron_job, db_name)
    else:
        # Production environment: Cron job runs every Sunday at 23:00
        schedule.every().sunday.at("23:00").do(cron_job, db_name)
    while True:
        schedule.run_pending()
        time.sleep(1)



# Start the Streamlit server
def run_streamlit():
    # Streamlit command-line arguments configuration based on environment
    if local_env:
        # Local environment: Set up for debugging on port 8501
        sys.argv = ["streamlit", "run", "nutritrack/web/main.py", db_name, "--server.port", "8501"]
    else:
        # Production environment: Configure for production server on port 32223
        sys.argv = ["streamlit", "run", "web/main.py", db_name, "--server.port", "32223"]
    stcli.main()

# Main function to start parallel processes
if __name__ == "__main__":
    # Start the cron job scheduler and Streamlit server in parallel
    access_db()
    cron_process = multiprocessing.Process(target=schedule_cron, args=(db_name,))
    streamlit_process = multiprocessing.Process(target=run_streamlit)

    cron_process.start()
    streamlit_process.start()

    # Wait for both processes to complete (blocking call)
    cron_process.join()
    streamlit_process.join()
