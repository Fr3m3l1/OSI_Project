from streamlit_js_eval import streamlit_js_eval
import streamlit as st
import hashlib
import sqlite3
import time

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize session state if not done already
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Database setup
DB_NAME = "nutrition_data.db"

# Database functions
def add_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", 
                   (username, hash_password(password)))
    conn.commit()
    conn.close()

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

# Helper function to manage URL-based navigation
def navigate_to(page_name):
    st.query_params["page"] = page_name

def refresh():
    time.sleep(0.2)
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

# Function to display the dashboard
def dashboard():
    user = st.session_state.current_user
    user_data = get_user_data(user)
    
    st.title(f"Welcome {user} to your Dashboard!")

# Main application logic
st.title("Nutrition Tracker")

# URL navigation setup
page = st.query_params.page
if page is None or page == "":
    page = "Login"

# Sidebar navigation
if st.session_state.logged_in:
    menu = ["Dashboard", "Log Out"]
else:
    menu = ["Login", "Sign Up"]

if page in menu:
    selected_page = st.sidebar.radio("Select a page", menu, index=menu.index(page))
else:
    selected_page = "Login"
    print("Invalid page selected. Redirecting to Login page.")
    print(st.session_state.logged_in)

# Page routing based on sidebar selection or URL parameter
if selected_page == "Login":
    navigate_to("Login")
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Login successful!")
            navigate_to("Dashboard")
            refresh()
        else:
            st.error("Invalid username or password.")

elif selected_page == "Sign Up":
    navigate_to("Sign Up")
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        if login_user(username, password) is None:
            add_user(username, password)
            st.success("Sign-up successful! You can now log in.")
            navigate_to("Login")
        else:
            st.error("User already exists. Please choose a different username.")

elif selected_page == "Dashboard" and st.session_state.logged_in:
    navigate_to("Dashboard")
    dashboard()

# Logout functionality
if selected_page == "Log Out" and st.session_state.logged_in:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("Logged out successfully!")
    navigate_to("Login")
