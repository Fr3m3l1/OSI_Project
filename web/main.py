from streamlit_js_eval import streamlit_js_eval
from streamlit_cookies_controller import CookieController
import streamlit as st
import hashlib
import sqlite3
import time

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Database setup
DB_NAME = "nutrition_data.db"
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

def get_user_data(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

# Cookie management
def set_cookie(name, value, expires=None):
    controller.set(name, value, max_age=expires, path="/")

def get_cookie(name):
    return controller.get(name)

def delete_cookie(name):
    controller.remove(name)

def navigate_to(page_name):
    st.query_params.page = page_name
    time.sleep(0.2)
    st.rerun()

# Function to display the dashboard
def dashboard():
    user = get_cookie("current_user")
    user_data = get_user_data(user)
    st.title(f"Welcome {user} to your Dashboard!")

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
    print("Invalid page selected. Redirecting to Dashboard.")
    page = "Dashboard"
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
