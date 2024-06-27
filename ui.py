import streamlit as st
import datetime
import os
import pandas as pd

from config import exercise_defaults, flat_exercise_defaults, get_bigquery_client
from data import save_to_csv, upload_to_bigquery

from dotenv import load_dotenv
from config import get_bigquery_client, cardio_exercises
# Load environment variables
load_dotenv()

# ui.py

def display_home():
    st.header("Welcome to the Fitness Tracker App")
    st.write("Use this app to log your workouts and track your progress over time.")
    st.image("images/pilate.webp", use_column_width=True)

def display_log_workout():
    st.header("Log a Workout")
    
    # Date input
    date = st.date_input("Date", datetime.date.today())
    
    # Select exercise group
    group = st.selectbox("Exercise Group", list(exercise_defaults.keys()))
    
    # Select exercise from the chosen group
    exercise = st.selectbox("Exercise", list(exercise_defaults[group].keys()))
    
    # Get default sets and reps for the selected exercise
    default_sets, default_reps_min, default_reps_max = flat_exercise_defaults[exercise]
    
    # Display recommended sets and reps as placeholders
    if default_reps_max == 'Failure':
        st.write(f"Recommended: {default_sets} sets to failure")
    else:
        st.write(f"Recommended: {default_sets} sets of {default_reps_min}-{default_reps_max} reps")
    
    # Input fields for sets
    sets = st.number_input("Sets", min_value=1, value=default_sets, help=f"Recommended: {default_sets} sets")
    
    # Generate input fields for each set's reps and weight
    reps_weights = []
    for set_num in range(1, sets + 1):
        st.write(f"Set {set_num}")
        reps = st.number_input(f"Reps for Set {set_num}", min_value=1, key=f"reps_{set_num}")
        weight = st.number_input(f"Weight (kg) for Set {set_num}", min_value=0, key=f"weight_{set_num}")
        reps_weights.append((reps, weight))
    
    # Submit button
    if st.button("Log Workout"):
        new_rows = []
        for set_num, (reps, weight) in enumerate(reps_weights, start=1):
            new_data = {
                'Date': date.strftime('%Y-%m-%d'),  # Ensure date is formatted as YYYY-MM-DD
                'Exercise': exercise,
                'Sets': set_num,  # Corrected field name
                'Reps': reps,
                'Weight': weight  # Ensured Weight is a float
            }
            new_rows.append(new_data)
            st.session_state.workout_data = pd.concat([st.session_state.workout_data, pd.DataFrame([new_data])], ignore_index=True)
        
        # Save the new rows to a CSV file
        save_to_csv(new_rows, 'workout_log.csv')
        
        st.success("Workout logged successfully!")

def display_log_measurement():
    st.header("Log Body Measurements")
    
    # Date input
    date = st.date_input("Date", datetime.date.today(), key='measurement_date')
    
    # Input fields for body measurements
    weight = st.number_input("Weight (kg)", min_value=0.0, key='measurement_weight')
    body_fat = st.number_input("Body Fat (%)", min_value=0.0, key='measurement_body_fat')
    chest = st.number_input("Chest (cm)", min_value=0.0, key='measurement_chest')
    waist = st.number_input("Waist (cm)", min_value=0.0, key='measurement_waist')
    hips = st.number_input("Hips (cm)", min_value=0.0, key='measurement_hips')
    
    # Submit button
    if st.button("Log Measurements"):
        new_measurement = {
            'Date': date.strftime('%Y-%m-%d'),
            'Weight': weight,
            'Body Fat': body_fat,
            'Chest': chest,
            'Waist': waist,
            'Hips': hips
        }
        st.session_state.body_measurements = pd.concat([st.session_state.body_measurements, pd.DataFrame([new_measurement])], ignore_index=True)
        
        # Save the new rows to a CSV file
        save_to_csv([new_measurement], 'body_measurements_log.csv')
        
        st.success("Measurements logged successfully!")

def display_view_progress():
    st.header("View Your Progress")
    
    # Load data from BigQuery
    client = get_bigquery_client()
    user_info = st.session_state.user_info
    sanitized_email = user_info['sanitized_email']
    
    workout_query = f"""
    SELECT * FROM `bubbly-trail-400312.fitness_logs.{sanitized_email}_workout`
    ORDER BY Date DESC
    """
    workout_data = client.query(workout_query).to_dataframe()
    
    st.subheader("Workout History")
    st.write(workout_data)
    
    measurement_query = f"""
    SELECT * FROM `bubbly-trail-400312.fitness_logs.{sanitized_email}_bodymeasurements`
    ORDER BY Date DESC
    """
    measurement_data = client.query(measurement_query).to_dataframe()
    
    st.subheader("Body Measurements")
    st.write(measurement_data)
    
    cardio_query = f"""
    SELECT * FROM `bubbly-trail-400312.fitness_logs.{sanitized_email}_cardio`
    ORDER BY Date DESC
    """
    cardio_data = client.query(cardio_query).to_dataframe()
    
    st.subheader("Cardio History")
    st.write(cardio_data)

def display_log_cardio():
    st.header("Log Cardio")

    # Date input
    date = st.date_input("Date", datetime.date.today())

    # Select cardio exercise
    exercise = st.selectbox("Cardio Exercise", list(cardio_exercises.keys()))

    # Input field for time in minutes
    time = st.number_input("Time (minutes)", min_value=1, help="Enter the duration of the cardio exercise in minutes")

    # Submit button
    if st.button("Log Cardio"):
        new_data = {
            'Date': date.strftime('%Y-%m-%d'),  # Ensure date is formatted as YYYY-MM-DD
            'Exercise': exercise,
            'Time': time  # Log the time for the cardio exercise
        }
        st.session_state.workout_data = pd.concat([st.session_state.workout_data, pd.DataFrame([new_data])], ignore_index=True)

        # Save the new rows to a CSV file
        save_to_csv([new_data], 'cardio_log.csv')

        st.success("Cardio logged successfully!")
