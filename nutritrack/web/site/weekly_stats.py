import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from web.helper.userHandling import get_user_weekly_stats


def weekly_stats(DB_NAME, user_id):
    st.title("Weekly Nutrition Statistics")

    # Fetch the weekly stats
    stats = get_user_weekly_stats(user_id, DB_NAME)

    # Check if data is available
    if not stats:
        st.write("No statistics available for the selected user.")
        return
    
    if isinstance(stats, tuple):  # Single tuple returned
        stats = [stats]
    
    # Convert the data to a DataFrame for easier plotting from the database (ID, Week ID, Year, User ID, Week Start Date, Total Calories, Total Protein, Total Carbs, Total Fats)
    df = pd.DataFrame(stats, columns=["ID", "Week ID", "Year", "User ID", "Week Start", "Calories", "Protein", "Carbs", "Fats"])

    # Plot the data
    st.write("### Weekly Nutrition Trends")
    fig, ax = plt.subplots(figsize=(10, 6))  # Set the figure size for better readability

    # Plot each metric
    ax.plot(df["Week Start"], df["Calories"], marker='o', label="Calories", linewidth=2)
    ax.plot(df["Week Start"], df["Protein"], marker='o', label="Protein", linewidth=2)
    ax.plot(df["Week Start"], df["Carbs"], marker='o', label="Carbs", linewidth=2)
    ax.plot(df["Week Start"], df["Fats"], marker='o', label="Fats", linewidth=2)

    # Beautify the plot
    ax.set_xlabel("Week Start", fontsize=12)
    ax.set_ylabel("Amount", fontsize=12)
    ax.set_title("Weekly Nutrition Trends", fontsize=16, fontweight='bold')
    ax.legend(title="Metrics", fontsize=10)  
    ax.grid(visible=True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.tick_params(axis='both', which='major', labelsize=10)

    # Display the plot
    st.pyplot(fig)
