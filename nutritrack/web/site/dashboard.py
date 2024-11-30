# Function to display the dashboard
import streamlit as st
import pandas as pd
from processor.data_checker import fetch_and_store_nutrition_data
from web.helper.cookies import get_cookie
from web.helper.userHandling import get_user_data_weekConsumed
from web.helper.miscellaneous import navigate_to

def dashboard(DB_NAME):
    user = get_cookie("current_user")
    user_data = get_user_data_weekConsumed(get_cookie("user_id"), DB_NAME)

    st.write(f"## Welcome {user} to your Dashboard!")

    if user_data:
        st.write(f"Hello {user}, here's your data for this week:")
        # Format the data into a table for better readability 
        # Add column name (product_name, calories, protein, carbs, fats, amount, consume_date)
        headers_name = ["Product Name", "Calories", "Protein", "Carbs", "Fats", "Amount", "Consume Date"]
        # Transpose the data to display in a table from row to column
        df = pd.DataFrame(user_data, columns=headers_name)
        st.write(df)
        
    else:
        st.write("No data found for this week.")

    # Add input field to search for food items
    search_query = st.text_input("Enter a food item to search:")
    amount = st.number_input("Enter the amount consumed (in grams):", min_value=0, value=100)
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Enter the date consumed:")
    with col2:
        time_consumed = st.time_input("Enter the time consumed:")
    if st.button("Add"):
        data_time = f"{date} {time_consumed}"
        # Fetch and store nutrition data
        err = fetch_and_store_nutrition_data(DB_NAME, search_query, data_time, get_cookie("user_id"), amount)
        if err:
            st.error("No data found for the given query.")
        else:
            st.success("Data fetched and stored successfully!")
            # Show reload button
            if st.button("Reload Page"):
                navigate_to("Dashboard")
