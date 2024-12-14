import multiprocessing
import streamlit.web.cli as stcli
import schedule
import time
import sys
import os
import logging
from dotenv import load_dotenv
from processor.cron_job import cron_job_weekly_stats, cron_job_backup_meltano

from data import create_nutrition_table

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
# Color codes for logging
logging.addLevelName(logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

# Load environment variables from .env file
load_dotenv()
# Check if local enviroment is set
if os.getenv("ENV") == "Local":
    db_name = "nutritrack/data/nutrition_data.db"
    local_env = True
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logging.warning("Running in local environment.")
else:
    db_name = "data/nutrition_data.db"
    local_env = False
    # Set up logging
    logging.basicConfig(level=logging.WARNING)
    logging.info("Running in production environment.")

# Access the SQLite database
def access_db():
    create_nutrition_table.create_table(db_name)

# Function to execute Meltano jobs
def run_meltano_job():
    logging.info("Running Meltano job...")
    # Create backup folder if it doesn't exist
    if not local_env and not os.path.exists("data/backup_data"):
        os.makedirs("data/backup_data")
    elif local_env and not os.path.exists("nutritrack/data/backup_data"):
        os.makedirs("nutritrack/data/backup_data")

    try:
        # Run the Meltano job specified in the 'daily_csv_backup' schedule
        if local_env:
            os.system("cd nutritrack/backup_meltano/project && meltano el tap-csv target-sqlite")
        else:
            os.system("cd backup_meltano/project && meltano el tap-csv target-sqlite --log-level=warning")
            logging.info("Meltano job executed.")
    except Exception as e:
        logging.error(f"Error running Meltano job: {e}")

# Function to schedule tasks
def schedule_cron(db_name):
    if local_env:
        schedule.every(5).minutes.do(cron_job_weekly_stats, db_name)
        schedule.every(1).minutes.do(cron_job_backup_meltano, db_name)
        schedule.every(2).minutes.do(run_meltano_job)
    else:
        schedule.every().sunday.at("23:00").do(cron_job_weekly_stats, db_name)
        schedule.every().day.at("22:00").do(cron_job_backup_meltano, db_name)
        schedule.every().day.at("22:30").do(run_meltano_job)
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
