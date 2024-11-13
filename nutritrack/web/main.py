from streamlit_cookies_controller import CookieController
import streamlit as st
import hashlib
import sqlite3
import time
import pandas as pd
import sys

from processor.data_checker import fetch_and_store_nutrition_data
from web.helper.cookies import set_cookie, get_cookie, delete_cookie

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Database setup
print(f"Database path: {sys.argv[1]}")
DB_NAME = sys.argv[1]
controller = CookieController()

# Database functions
def add_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Check if user already exists
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return False
    cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", 
                   (username, hash_password(password)))
    conn.commit()
    conn.close()
    return True

def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[2] == hash_password(password):  # user[2] is the password column
        return user
    return None

def get_user_data_weekConsumed(user_id_value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.product_name, p.calories, p.protein, p.carbs, p.fats, k.amount, k.consume_date
        FROM Konsumiert k
        JOIN Product p ON k.product_id = p.product_id
        WHERE k.consume_date >= datetime('now', '-7 days')
        AND k.user_id = ?
    ''', (user_id_value,))
    user_data = cursor.fetchall()
    conn.close()
    return user_data

def navigate_to(page_name):
    st.query_params.page = page_name
    time.sleep(0.2)
    st.rerun()

# Function to display the dashboard
def dashboard():
    user = get_cookie("current_user")
    user_data = get_user_data_weekConsumed(get_cookie("user_id"))

    st.title(f"Welcome {user} to your Dashboard!")

    if user_data:
        st.write(f"Hello {user}, here's your data for the past week:")
        # Format the data into a table for better readability 
        # Add column name (product_name, calories, protein, carbs, fats, amount, consume_date)
        headers_name = ["Product Name", "Calories", "Protein", "Carbs", "Fats", "Amount", "Consume Date"]
        # Transpose the data to display in a table from row to column
        df = pd.DataFrame(user_data, columns=headers_name)
        st.write(df)
        
    else:
        st.write("No data found for the past week.")

    # Add input field to search for food items
    search_query = st.text_input("Enter a food item to search:")
    if st.button("Search"):
        # Fetch and store nutrition data
        err = fetch_and_store_nutrition_data(DB_NAME, search_query, get_cookie("user_id"))
        if err:
            st.error("No data found for the given query.")
        else:
            st.success("Data fetched and stored successfully!")
            # Show reload button
            if st.button("Reload Page"):
                navigate_to("Dashboard")


# Main application logic
st.title("Nutrition Tracker")

# URL navigation setup
try:
    page = st.query_params.page
except AttributeError:
    print("No query params found.")
    page = "Login"

# Retrieve login status from cookie
logged_in = get_cookie("logged_in") == "true"

# Sidebar navigation
if logged_in:
    menu = ["Dashboard", "Log Out"]
else:
    menu = ["Login", "Sign Up"]

# Page routing
try:
    selected_page = st.sidebar.radio("Select a page", menu, index=menu.index(page))
    if selected_page != page:
        navigate_to(selected_page)
except ValueError:
    print(f"Invalid match for page: {page} in menu: {menu}")
    page = "Login"
    selected_page = st.sidebar.radio("Select a page", menu, index=menu.index(page))

if selected_page == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            set_cookie("logged_in", "true")
            set_cookie("current_user", username)
            set_cookie("user_id", user[0])
            st.success("Login successful!")
            navigate_to("Dashboard")
        else:
            st.error("Invalid username or password.")

elif selected_page == "Sign Up":
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        if login_user(username, password) is None:
            if add_user(username, password):
                st.success("Sign-up successful! You can now log in.")
                time.sleep(2)
                navigate_to("Login")
            else:
                st.error("User already exists. Please choose a different username.")
        else:
            st.error("User already exists. Please choose a different username.")

elif selected_page == "Dashboard" and logged_in:
    dashboard()

# Logout functionality
if selected_page == "Log Out" and logged_in:
    delete_cookie("logged_in")
    delete_cookie("current_user")
    st.success("Logged out successfully!")
    time.sleep(2)
    navigate_to("Login")
