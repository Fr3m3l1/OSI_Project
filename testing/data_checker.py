# fetch_and_insert_data
import sqlite3
from testing.nutritionix_api import NutritionixAPI

# Initialize NutritionixAPI
api = NutritionixAPI()

# Function to insert data into the SQLite database
def insert_nutrition_data(db_name, food_data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Product (barcode, product_name, calories, protein, carbs, fats, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (food_data.get('barcode', None), 
          food_data['food'], 
          food_data['calories'], 
          food_data['protein'], 
          food_data['carbs'], 
          food_data['fats']))
    conn.commit()
    conn.close()
    print(f"Data for {food_data['food']} inserted into the database.")

# Function to fetch and insert nutrition data based on user input
def fetch_and_store_nutrition_data(db_name, query):
    # Fetch data using NutritionixAPI
    nutrition_data = api.get_nutrition_info(query)
    
    # Insert each item into the database
    if nutrition_data:
        for item in nutrition_data:
            insert_nutrition_data(db_name, item)
    else:
        print("No data found for the given query.")

# Example usage
if __name__ == "__main__":
    # Ensure the database has been created by running create_nutrition_table.py first
    query = input("Enter a food item to search: ")
    fetch_and_store_nutrition_data("nutrition_data.db", query)
