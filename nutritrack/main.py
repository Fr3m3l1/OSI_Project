import multiprocessing
import streamlit.web.cli as stcli
import schedule
import time
import sys
import os
from dotenv import load_dotenv
from processor.cron_job import cron_job

from data import create_nutrition_table




# Load environment variables from .env file
load_dotenv()
# Check if local enviroment is set
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

# Function to schedule tasks
def schedule_cron(db_name):
    if local_env:
        schedule.every(1).minutes.do(cron_job, db_name)
    else:
        schedule.every().sunday.at("23:00").do(cron_job, db_name)
    while True:
        schedule.run_pending()
        time.sleep(1)



# Function to start the Streamlit server
def run_streamlit():
    if local_env:
        sys.argv = ["streamlit", "run", "nutritrack/web/main.py", db_name, "--server.port", "8501"]
    else:
        sys.argv = ["streamlit", "run", "web/main.py", db_name, "--server.port", "32223"]
    stcli.main()

# Main function to start processes
if __name__ == "__main__":
    # Start the cron job scheduler and Streamlit server in parallel
    access_db()
    cron_process = multiprocessing.Process(target=schedule_cron, args=(db_name,))
    streamlit_process = multiprocessing.Process(target=run_streamlit)

    cron_process.start()
    streamlit_process.start()

    cron_process.join()
    streamlit_process.join()
