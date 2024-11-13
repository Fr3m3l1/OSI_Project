import streamlit as st
import hashlib
import sqlite3

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize session state if not done already
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Function to handle login
def login(username, password):
    if username in st.session_state.user_data:
        stored_password_hash = st.session_state.user_data[username]['password']
        if stored_password_hash == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Login successful!")
        else:
            st.error("Incorrect password.")
    else:
        st.error("User not found.")

# Function to add a new user
def add_user(username, password):
    conn = sqlite3.connect("nutrition_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", 
                   (username, hash_password(password)))
    conn.commit()
    conn.close()

# Function to check if a user exists and validate password
def login_user(username, password):
    conn = sqlite3.connect("nutrition_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[2] == hash_password(password):  # user[2] is the password column
        return user
    return None

# Function to get user data for the dashboard
def get_user_data(username):
    conn = sqlite3.connect("nutrition_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT calories, nutrition FROM Users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


# Function to display the dashboard
def dashboard():
    user = st.session_state.current_user
    nutrition = st.session_state.user_data[user].get('nutrition', 0)
    calories = st.session_state.user_data[user].get('calories', 0)
    
    st.title(f"Welcome {user} to your Dashboard!")
    st.write(f"Nutrition Consumed: {nutrition}g")
    st.write(f"Calories Consumed: {calories} kcal")

# Main application logic
st.title("Nutrition Tracker")

# Sidebar navigation
if st.session_state.logged_in:
    menu = ["Dashboard", "Log Out"]
else:
    menu = ["Login", "Sign Up"]

page = st.sidebar.radio("Select a page", menu)

if page == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

elif page == "Sign Up":
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        # Check if the user already exists
        if login_user(username, password) is None:
            add_user(username, password)
            st.success("Sign-up successful! You can now log in.")
        else:
            st.error("User already exists. Please choose a different username.")

elif page == "Dashboard" and st.session_state.logged_in:
    dashboard()

# Logout functionality
if page == "Log Out" and st.session_state.logged_in:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("Logged out successfully!")
