import hashlib
import time
import streamlit as st

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def navigate_to(page_name):
    st.query_params.page = page_name
    time.sleep(0.2)
    st.rerun()