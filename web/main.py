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

# Function to handle sign-up
def sign_up(username, password):
    if username in st.session_state.user_data:
        st.error("User already exists.")
    else:
        st.session_state.user_data[username] = {'password': hash_password(password), 'nutrition': 0, 'calories': 0}
        st.success("Sign-up successful! You can now log in.")

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
        login(username, password)

elif page == "Sign Up":
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        sign_up(username, password)

elif page == "Dashboard":
    dashboard()

# Logout functionality
if page == "Log Out" and st.session_state.logged_in:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("Logged out successfully!")
