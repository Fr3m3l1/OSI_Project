import os
import requests

# Retrieve API credentials from environment variables
APP_ID = os.getenv("NUTRITIONIX_APP_ID")
API_KEY = os.getenv("NUTRITIONIX_API_KEY")

# Verify that APP_ID and API_KEY are loaded correctly
if not APP_ID or not API_KEY:
    print("Error: API credentials are missing. Check your .env file.")
    exit()

class NutritionixAPI:
    def __init__(self):
        self.url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        self.headers = {
            "x-app-id": APP_ID,
            "x-app-key": API_KEY,
            "Content-Type": "application/json"
        }

    def get_nutrition_data(self, query):
        response = requests.post(self.url, headers=self.headers, json={"query": query})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.json().get('message', 'Unknown error')}")
            return None

    def get_nutrition_info(self, query):
        data = self.get_nutrition_data(query)
        if data and 'foods' in data:
            info = []
            for food in data['foods']:
                info.append({
                    "food": food['food_name'],
                    "calories": food['nf_calories'],
                    "protein": food['nf_protein'],
                    "carbs": food['nf_total_carbohydrate'],
                    "fats": food['nf_total_fat']
                })
            return info
        else:
            print("No data found for the given query.")
            return None

    def get_summary(self, query):
        data = self.get_nutrition_data(query)
        if not data or 'foods' not in data:
            print("No data available to summarize.")
            return {}

        summaries = {}
        for food in data['foods']:
            for key, value in food.items():
                if key in ["nf_calories", "nf_protein", "nf_total_carbohydrate", "nf_total_fat"]:
                    summaries[key] = summaries.get(key, 0) + value

        # Rename keys to simplified names and round values
        summaries = {
            "calories": round(summaries.get("nf_calories", 0), 2),
            "protein": round(summaries.get("nf_protein", 0), 2),
            "carbs": round(summaries.get("nf_total_carbohydrate", 0), 2),
            "fats": round(summaries.get("nf_total_fat", 0), 2)
        }
        
        return summaries

# Test the API class with a sample query
if __name__ == "__main__":
    api = NutritionixAPI()
    
    # Test fetching detailed nutrition info
    query = "1 cup of rice and 2 eggs"
    print("Fetching detailed nutrition info:")
    nutrition_info = api.get_nutrition_info(query)
    if nutrition_info:
        for item in nutrition_info:
            print(item)

    # Test fetching summary info
    print("\nFetching summary nutrition info:")
    summary_info = api.get_summary(query)
    if summary_info:
        print("Summary:", summary_info)
