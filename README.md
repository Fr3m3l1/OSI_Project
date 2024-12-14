# OSI_Project

## Project Name
Nutritrack

## Description
This project is a nutrition tracking application that allows users to track their daily food intake. The application will provide users with a daily calorie goal based on their personal information. Users will be able to add consumed foods to their daily log and the application will calculate the total calories consumed. 

## Team Members
- [grahanoi](https://github.com/grahanoi)
- [gurovamr](https://github.com/gurovamr)
- [schmic05](https://github.com/Fr3m3l1)
- [laglepia](https://github.com/Lagpi)

## Infrastructure
- Portman (Container)
- Streamlit (Flask)
- SQLite
- Nutrionix API
- Cron Job (Weekly Statistics)
- Backup with Meltano 

![Infrastructure](https://github.com/Fr3m3l1/OSI_Project/blob/main/doc/Infrastucture%20Plan.png)

![DB Schema](https://github.com/Fr3m3l1/OSI_Project/blob/main/doc/DB%20Structure.png)


## Steps to run the application
1. Clone the repository
2. Create a virtual environment and activate it
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Run the following command to install the required packages:
```bash
pip install -r requirements.txt
```
4. Create a .env file in the /nutrirack directory of the project and add the following environment variables:
```bash
NUTRITIONIX_APP_ID=YOUR_NUTRITIONIX_APP_ID
NUTRITIONIX_API_KEY=YOUR_NUTRITIONIX
```
5. Be in the root directory of the project and run the following command:
```bash
python nutritrack/main.py
```