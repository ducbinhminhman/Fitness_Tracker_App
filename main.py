import streamlit as st
import pandas as pd
import re
import os

from config import get_bigquery_client, exercise_defaults, flat_exercise_defaults
from ui import display_home, display_log_workout, display_view_progress, display_log_measurement
from data import upload_to_bigquery

# Initialize session state
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = pd.DataFrame(columns=['Date', 'Exercise', 'Sets', 'Reps', 'Weight'])

if 'body_measurements' not in st.session_state:
    st.session_state.body_measurements = pd.DataFrame(columns=['Date', 'Weight', 'Body Fat', 'Chest', 'Waist', 'Hips'])

if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

def login():
    st.header("Login")
    user_name = st.text_input("Username")
    user_email = st.text_input("Email")

    if st.button("Login"):
        if user_name and user_email:
            sanitized_email = re.sub(r'[^a-z0-9]', '_', user_email.lower())
            st.session_state.user_info = {
                'user_name': user_name,
                'user_email': user_email,
                'sanitized_email': sanitized_email
            }
            st.success("Login successful!")
            st.experimental_rerun()  # Trigger rerun to refresh the app with navigation

# Title and Description
st.title("Fitness Tracker App")
st.write("Track your workout history, weight, body measurements, and other fitness metrics over time.")

# Login Section
if 'user_name' not in st.session_state.user_info:
    login()
else:
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox("Choose a section", ["Home", "Log Workout", "Log Measurement", "View Progress"])

    # Navigation logic
    if option == "Home":
        display_home()
    elif option == "Log Workout":
        display_log_workout()
    elif option == "Log Measurement":
        display_log_measurement()
    elif option == "View Progress":
        display_view_progress()

    # Upload to BigQuery
    if st.sidebar.button("Upload to BigQuery"):
        client = get_bigquery_client("C:/Users/mandu/Desktop/Privat_key/bubbly-trail-400312-281c05bdd2e4.json")
        user_name = st.session_state.user_info['user_name']
        sanitized_email = st.session_state.user_info['sanitized_email']
        
        workout_csv_file = 'workout_log.csv'
        if os.path.exists(workout_csv_file):
            workout_table_id = f"{user_name}_{sanitized_email}_workout"
            upload_to_bigquery(client, workout_table_id, workout_csv_file)
            st.success("Workout data uploaded to BigQuery successfully!")
        else:
            st.error("No workout data available to upload.")
        
        measurement_csv_file = 'body_measurements_log.csv'
        if os.path.exists(measurement_csv_file):
            measurement_table_id = f"{user_name}_{sanitized_email}_bodymeasurements"
            upload_to_bigquery(client, measurement_table_id, measurement_csv_file)
            st.success("Body measurements data uploaded to BigQuery successfully!")
        else:
            st.error("No body measurements data available to upload.")
