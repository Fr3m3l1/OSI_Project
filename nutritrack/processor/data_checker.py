# fetch_and_insert_data
import sqlite3
from processor.API.nutritionix_api import NutritionixAPI

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
          food_data['food'].upper(), 
          food_data['calories'], 
          food_data['protein'], 
          food_data['carbs'], 
          food_data['fats']))
    conn.commit()
    conn.close()
    print(f"Data for {food_data['food']} inserted into the database.")

def search_product(query, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Product WHERE product_name = ?", (query,))
    product = cursor.fetchone()
    conn.close()
    return product

def check_duplicate(query, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Product WHERE product_name = ?", (query,))
    product = cursor.fetchone()
    conn.close()
    if product:
        return [True, product]
    return [False, None]

# Function to fetch and insert nutrition data based on user input
def fetch_and_store_nutrition_data(db_name, query, user_id = None, amount = 1) -> Exception:
    # Fetch data using NutritionixAPI
    print(f"Fetching data for: {query}")

    # Split the query into individual words
    query_array = query.split()

    for i in range(len(query_array)):
        # Upper case all the words
        query_string = query_array[i]
        query_string = query_string.upper()
        print(f"Checking for: {query_string}")

        is_duplicate, product = check_duplicate(query_string, db_name)

        print(f"Is duplicate: {is_duplicate}")

        # Check if the word is in the database
        if not is_duplicate:
            nutrition_data = api.get_nutrition_info(query_string)
            # Insert each item into the database
            if nutrition_data:
                for item in nutrition_data:
                    insert_nutrition_data(db_name, item)
                product = search_product(query_string, db_name)
            else:
                print("No data found for the given query.")
                return Exception("No data found for the given query.")

        if user_id != None:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Konsumiert (user_id, product_id, amount)
                VALUES (?, ?, ?)
            ''', (user_id, product[0], amount))
            conn.commit()
            conn.close()

    return None
        


# Example usage
if __name__ == "__main__":
    # Ensure the database has been created by running create_nutrition_table.py first
    query = input("Enter a food item to search: ")
    fetch_and_store_nutrition_data("nutrition_data.db", query)
