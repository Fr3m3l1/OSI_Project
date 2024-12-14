from streamlit_cookies_controller import CookieController
import streamlit as st
import time
import sys
import logging

from web.helper.cookies import set_cookie, get_cookie, delete_cookie
from web.helper.userHandling import login_user, add_user
from web.helper.miscellaneous import navigate_to
from web.site.dashboard import dashboard
from web.site.weekly_stats import weekly_stats
from web.site.data import data_editor

# Database setup
DB_NAME = sys.argv[1]
try:
    controller = CookieController()
except FileNotFoundError:
    logging.error("No cookies found.")
    controller = CookieController()
except Exception as e:
    logging.error(f"Error: {e}")
    controller = CookieController()

# Main application logic
st.title("Nutrition Tracker")

# URL navigation setup
try:
    page = st.query_params.page
except AttributeError:
    logging.warning("No query params found.")
    page = "Login"

# Retrieve login status from cookie
logged_in = get_cookie("logged_in") == "true"

# Sidebar navigation
if logged_in:
    menu = ["Dashboard", "Weekly Stats", "Data", "Log Out"]
else:
    menu = ["Login", "Sign Up"]

# Page routing
try:
    selected_page = st.sidebar.radio("Select a page", menu, index=menu.index(page))
    if selected_page != page:
        navigate_to(selected_page)
except ValueError:
    logging.warning(f"Invalid match for page: {page} in menu: {menu}")
    page = "Login"
    selected_page = st.sidebar.radio("Select a page", menu, index=menu.index(page))

logging.debug("Selected page:", selected_page)

if selected_page == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login") or st.session_state.get("login_enter_pressed", True):
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

    if st.button("Sign Up") or st.session_state.get("signup_enter_pressed", True):
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
    weekly_stats(DB_NAME, get_cookie("user_id"))

elif selected_page == "Data" and logged_in:
    data_editor(DB_NAME, get_cookie("user_id"))

# Logout functionality
if selected_page == "Log Out" and logged_in:
    delete_cookie("logged_in")
    delete_cookie("current_user")
    st.success("Logged out successfully!")
    time.sleep(2)
    navigate_to("Login")
