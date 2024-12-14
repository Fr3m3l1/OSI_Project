import streamlit as st
import pandas as pd
from processor.data_checker import fetch_and_store_nutrition_data
from web.helper.userHandling import get_user_data, delete_user_data
from web.helper.miscellaneous import navigate_to

def data_editor(DB_NAME, user_id):
    """
    Function to display the data and allow the user to delete entries
    """
    st.title("Data Editor")

    # Fetch the user data
    user_data = get_user_data(DB_NAME, user_id)

    # Check if data is available
    if not user_data:
        st.write("No data available for the selected user.")
        return

    if isinstance(user_data, tuple):  # Single tuple returned
        user_data = [user_data]

    headers_name = ["ID", "Product Name", "Calories", "Protein", "Carbs", "Fats", "Amount", "Consume Date"]
    
    # Data transpose
    df = pd.DataFrame(user_data, columns=headers_name)

    # Roun float columns to 2 decimal places
    df = df.round(2)
    
    # Data display
    st.write("### User Data")
    st.markdown(
        df.style.format(precision=2).hide(axis="index").to_html(),
        unsafe_allow_html=True
    )

    # Input field to delete entries
    st.write("### Delete Entries")
    delete_id = st.number_input("Enter the ID of the entry to delete:", min_value=0, value=0)
    if st.button("Delete"):
        err = delete_user_data(delete_id, DB_NAME, user_id)
        if err:
            st.error("No data found for the given ID.")
        else:
            st.success("Data deleted successfully!")
            # Reload button
            if st.button("Reload Page"):
                navigate_to("Data")