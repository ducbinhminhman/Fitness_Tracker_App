import os
from google.cloud import bigquery
from google.oauth2 import service_account

import json
from google.cloud import bigquery

def get_bigquery_client():
    credential_path = os.getenv('BIGQUERY_CREDENTIALS')
    client = bigquery.Client.from_service_account_json(credential_path)
    return client



# Define exercise groups and exercises with their default sets and reps
exercise_defaults = {
    "Push (Chest, Shoulders, Triceps)": {
        "Bench Press": (4, 6, 8),
        "Incline Dumbbell Press": (3, 8, 10),
        "Overhead Shoulder Press": (3, 8, 10),
        "Lateral Raises": (3, 12, 15),
        "Tricep Dips": (3, 0, 'Failure'),
        "Tricep Pushdowns": (3, 10, 12),
        "Incline Bench Press": (4, 6, 8),
        "Flat Dumbbell Press": (3, 8, 10),
        "Arnold Press": (3, 8, 10),
        "Front Raises": (3, 12, 15),
        "Skull Crushers": (3, 10, 12),
        "Overhead Tricep Extension": (3, 10, 12),
    },
    "Pull (Back, Biceps)": {
        "Deadlifts": (4, 6, 8),
        "Pull-Ups or Lat Pulldowns": (4, 6, 8),
        "Bent-Over Rows": (3, 8, 10),
        "Seated Cable Rows": (3, 10, 12),
        "Face Pulls": (3, 12, 15),
        "Bicep Curls": (3, 10, 12),
        "T-Bar Rows": (4, 6, 8),
        "Single-Arm Dumbbell Rows": (3, 8, 10),
        "Wide Grip Pull-Ups or Lat Pulldowns": (3, 8, 10),
        "Cable Rows": (3, 10, 12),
        "Rear Delt Flyes": (3, 12, 15),
        "Hammer Curls": (3, 10, 12),
    },
    "Legs (Quadriceps, Hamstrings, Glutes, Calves)": {
        "Squats": (4, 6, 8),
        "Leg Press": (3, 8, 10),
        "Romanian Deadlifts": (3, 8, 10),
        "Leg Curls": (3, 10, 12),
        "Calf Raises": (4, 12, 15),
    }
}

# Flatten the exercise_defaults to easily map exercises to their defaults
flat_exercise_defaults = {exercise: values for group in exercise_defaults.values() for exercise, values in group.items()}
