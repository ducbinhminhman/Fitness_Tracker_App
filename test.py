import streamlit as st
import datetime
import os
import pandas as pd

from config import exercise_defaults, flat_exercise_defaults, get_bigquery_client
from data import save_to_csv, upload_to_bigquery

def display_home():
    st.header("Welcome to the Fitness Tracker App")
    st.write("Use this app to log your workouts and track your progress over time.")

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
        csv_file = 'body_measurements_log.csv'
        pd.DataFrame([new_measurement]).to_csv(csv_file, index=False, mode='a', header=not os.path.exists(csv_file))
        
        # Upload to BigQuery
        client = get_bigquery_client("C:/Users/mandu/Desktop/Privat_key/bubbly-trail-400312-281c05bdd2e4.json")
        table_id = "bubbly-trail-400312.fitness_logs.body_measurements"
        upload_to_bigquery(client, table_id, csv_file)
        st.success("Measurements logged successfully!")
        
        # Remove the file if it exists
        if os.path.exists(csv_file):
            os.remove(csv_file)

def display_view_progress():
    st.header("View Your Progress")
    
    # Load data from BigQuery
    client = get_bigquery_client("C:/Users/mandu/Desktop/Privat_key/bubbly-trail-400312-281c05bdd2e4.json")
    
    workout_query = """
    SELECT * FROM `bubbly-trail-400312.fitness_logs.workout`
    ORDER BY Date DESC
    """
    workout_data = client.query(workout_query).to_dataframe()
    
    st.subheader("Workout History")
    st.write(workout_data)
    
    measurement_query = """
    SELECT * FROM `bubbly-trail-400312.fitness_logs.body_measurements`
    ORDER BY Date DESC
    """
    measurement_data = client.query(measurement_query).to_dataframe()
    
    st.subheader("Body Measurements")
    st.write(measurement_data)
