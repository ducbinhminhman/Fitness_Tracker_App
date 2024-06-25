import streamlit as st
import pandas as pd
import re
import os
from dotenv import load_dotenv

# Assuming these imports are correct as per your project structure
from config import exercise_defaults, flat_exercise_defaults, get_bigquery_client
from data import upload_to_bigquery
from ui import display_home, display_log_workout, display_log_measurement, display_view_progress

# Load environment variables
load_dotenv()

# Initialize session state
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = pd.DataFrame(columns=['Date', 'Exercise', 'Sets', 'Reps', 'Weight'])

if 'body_measurements' not in st.session_state:
    st.session_state.body_measurements = pd.DataFrame(columns=['Date', 'Weight', 'Body Fat', 'Chest', 'Waist', 'Hips'])

if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

def login():
    # Title and Description
    st.title("Fitness Tracker App")
    st.write("Track your workout history, weight, body measurements, and other fitness metrics over time.")
    # Display the image
    st.image("images/running.webp", use_column_width=True)
    st.header("Login")
    #user_name = st.text_input("Username")
    user_email = st.text_input("Email")

    if st.button("Login"):
        if user_email: #user_name and user_email:
            sanitized_email = re.sub(r'[^a-z0-9]', '_', user_email.lower())
            st.session_state.user_info = {
                #'user_name': user_name,
                'user_email': user_email,
                'sanitized_email': sanitized_email
            }
            st.experimental_rerun()  # Use experimental_rerun to reload the page and update the session state


# Login Section
if 'user_email' not in st.session_state.user_info:
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
        client = get_bigquery_client()
        #user_name = st.session_state.user_info['user_name']
        sanitized_email = st.session_state.user_info['sanitized_email']
        
        workout_csv_file = 'workout_log.csv'
        if os.path.exists(workout_csv_file):
            #workout_table_id = f"{user_name}_{sanitized_email}_workout"
            workout_table_id = f"{sanitized_email}_workout"
            upload_to_bigquery(client, workout_table_id, workout_csv_file)
            st.success("Workout data uploaded to BigQuery successfully!")
        else:
            st.error("No workout data available to upload.")
        
        measurement_csv_file = 'body_measurements_log.csv'
        if os.path.exists(measurement_csv_file):
            #measurement_table_id = f"{user_name}_{sanitized_email}_bodymeasurements"
            measurement_table_id = f"{sanitized_email}_bodymeasurements"
            upload_to_bigquery(client, measurement_table_id, measurement_csv_file)
            st.success("Body measurements data uploaded to BigQuery successfully!")
        else:
            st.error("No body measurements data available to upload.")
