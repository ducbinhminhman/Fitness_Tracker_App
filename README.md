# Fitness Tracker App Documentation

This guide explains the structure and usage of the Fitness Tracker App, built with Streamlit and Google BigQuery.

## Directory Structure

Your project should look like this:

```
Fitness_App/
├── main.py
├── config.py
├── data.py
├── ui.py
├── images/
│   ├── running.webp
│   └── pilate.webp
├── .env (optional, for environment variables)
├── workout_log.csv (optional, for data storage)
└── body_measurements_log.csv (optional, for data storage)
```

## File Overview

1. **`main.py`**: The main file to run the app. It initializes the app, manages navigation between different pages, and handles data upload to BigQuery.
2. **`config.py`**: Loads settings and exercise information. It includes the function to get the BigQuery client and defines the default exercise groups and exercises.
3. **`data.py`**: Manages data saving and uploading to BigQuery. It includes functions to save data to a CSV file and upload data to BigQuery.
4. **`ui.py`**: Contains the app's user interface. It includes functions to display the home page, log workouts, log body measurements, and view progress.

## Setup Instructions

### Prerequisites

- Install [Streamlit](https://docs.streamlit.io/library/get-started/installation):
  ```bash
  pip install streamlit
  ```
- Install the Google Cloud BigQuery library:
  ```bash
  pip install google-cloud-bigquery
  ```
- Install the Python dotenv library:
  ```bash
  pip install python-dotenv
  ```

### Configuration

1. **Google Cloud Credentials:**
   - Obtain your Google Cloud service account key JSON file and save it in a safe location, e.g., `C:/Users/mandu/Desktop/Privat_key/bubbly-trail-400312-281c05bdd2e4.json`.
   
2. **Environment Variables:**
   - Create a `.env` file in the root directory of your project and add the following line with the path to your Google Cloud credentials file:
     ```
     GOOGLE_APPLICATION_CREDENTIALS="C:/Users/mandu/Desktop/Privat_key/bubbly-trail-400312-281c05bdd2e4.json"
     ```
   - In the `.streamlit/secrets.toml` file, add the credentials dictionary:
     ```
     [credentials]
     type = "service_account"
     project_id = "your_project_id"
     private_key_id = "your_private_key_id"
     private_key = "your_private_key"
     client_email = "your_client_email"
     client_id = "your_client_id"
     auth_uri = "https://accounts.google.com/o/oauth2/auth"
     token_uri = "https://oauth2.googleapis.com/token"
     auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
     client_x509_cert_url = "your_client_x509_cert_url"
     ```

## Running the App

1. **Navigate to the Project Directory:**
   ```bash
   cd path/to/Fitness_App
   ```

2. **Run the Streamlit Application:**
   ```bash
   streamlit run main.py
   ```

## Using the App

### Home Page

- Displays a welcome message and an introductory image.

### Log Workout Page

- Allows users to log workout details including the date, exercise group, specific exercise, sets, reps, and weight.
- The data is saved to a CSV file (`workout_log.csv`).

### Log Measurement Page

- Allows users to log body measurements including date, weight, body fat percentage, chest, waist, and hips.
- The data is saved to a CSV file (`body_measurements_log.csv`).

### View Progress Page

- Allows users to view their workout history and body measurements.
- Fetches and displays data from Google BigQuery.

### Upload to BigQuery

- The sidebar includes a button to upload the logged data to Google BigQuery.
- Workout data is uploaded to a table named `<sanitized_email>_workout`.
- Body measurements data is uploaded to a table named `<sanitized_email>_bodymeasurements`.

## Code Explanation

### `config.py`
- **`get_bigquery_client()`**: Creates and returns a BigQuery client using credentials from environment variables.
- **Exercise Defaults**: Defines a dictionary with default sets and reps for various exercises grouped by exercise type.

### `data.py`
- **`save_to_csv(rows, filename)`**: Saves data rows to a CSV file. Appends to the file if it already exists.
- **`upload_to_bigquery(client, table_id, csv_file)`**: Uploads data from a CSV file to a specified BigQuery table. Defines the schema based on the table name and removes the CSV file after uploading.

### `main.py`
- **Login Functionality**: Provides a simple login mechanism using the user's email.
- **Session State Initialization**: Initializes session state variables for storing workout data, body measurements, and user information.
- **Navigation**: Manages navigation between different sections of the app (Home, Log Workout, Log Measurement, View Progress).
- **Data Upload**: Handles the process of uploading data to BigQuery.

### `ui.py`
- **`display_home()`**: Displays the home page with a welcome message and image.
- **`display_log_workout()`**: Displays the workout logging interface and saves the logged data.
- **`display_log_measurement()`**: Displays the body measurement logging interface and saves the logged data.
- **`display_view_progress()`**: Fetches and displays the user's workout history and body measurements from BigQuery.
