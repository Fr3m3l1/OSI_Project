from streamlit_cookies_controller import CookieController
import streamlit as st
import time
import sys

# Importing helper modules for various functionalities
from web.helper.cookies import set_cookie, get_cookie, delete_cookie
from web.helper.userHandling import login_user, add_user
from web.helper.miscellaneous import navigate_to
from web.site.dashboard import dashboard
from web.site.weekly_stats import weekly_stats
from web.site.data import data_editor

# Database setup
DB_NAME = sys.argv[1]

# Initialize the CookieController for managing session cookies
try:
    controller = CookieController()
except FileNotFoundError:
    print("No cookies found.")
    controller = CookieController()
except Exception as e:
    print(f"Error: {e}")
    controller = CookieController()

# Title of the application
st.title("Nutrition Tracker")

# Attempt to retrieve the current page from URL query parameters
try:
    page = st.query_params.page
except AttributeError:
    print("No query params found.")
    page = "Login"

# Retrieve login status from cookie
logged_in = get_cookie("logged_in") == "true"

# Define navigation menu based on the user's login status
if logged_in:
    menu = ["Dashboard", "Weekly Stats", "Data", "Log Out"]
else:
    menu = ["Login", "Sign Up"]

# Sidebar navigation setup
try:
    selected_page = st.sidebar.radio("Select a page", menu, index=menu.index(page))
    if selected_page != page:
        navigate_to(selected_page)
except ValueError:
    # Handle invalid or missing page query params
    print(f"Invalid match for page: {page} in menu: {menu}")
    page = "Login"
    selected_page = st.sidebar.radio("Select a page", menu, index=menu.index(page))

# Log the selected page for debugging purposes
print("Selected page:", selected_page)

# Page routing logic
if selected_page == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = login_user(username, password, DB_NAME)
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
        if login_user(username, password, DB_NAME) is None:
            if add_user(username, password, DB_NAME):
                st.success("Sign-up successful! You can now log in.")
                time.sleep(2)
                navigate_to("Login")
            else:
                st.error("User already exists. Please choose a different username.")
        else:
            st.error("User already exists. Please choose a different username.")

elif selected_page == "Dashboard" and logged_in:
    dashboard(DB_NAME)

elif selected_page == "Weekly Stats" and logged_in:
    # Weekly stats for the current user
    weekly_stats(DB_NAME, get_cookie("user_id"))

elif selected_page == "Data" and logged_in:
    # Data editor functionality for the current user
    data_editor(DB_NAME, get_cookie("user_id"))

# Logout functionality
if selected_page == "Log Out" and logged_in:
    delete_cookie("logged_in")
    delete_cookie("current_user")
    st.success("Logged out successfully!")
    time.sleep(2)
    navigate_to("Login")
