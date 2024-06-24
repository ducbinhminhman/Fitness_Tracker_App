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
└── workout_log.csv (optional, for data storage)
```

## File Overview

1. **`main.py`**: The main file to run the app.
2. **`config.py`**: Loads settings and exercise information.
3. **`data.py`**: Manages data saving and uploading to BigQuery.
4. **`ui.py`**: Contains the app's user interface.

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

### Configuration

1. **Google Cloud Credentials:**
   - Get your Google Cloud service account key JSON file and save it safely, e.g., `C:/Users/mandu/Desktop/Privat_key/bubbly-trail-400312-281c05bdd2e4.json`.

2. **Update `config.py`:**
   - Make sure the path to your Google Cloud credentials file is correct.

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

- Shows a welcome message.

### Log Workout Page

- Log workout details: date, exercise group, specific exercise, sets, reps, and weight.
- Data is saved to a CSV file.

### View Progress Page

- View logged workout history and body measurements.
- Log new body measurements.

### Upload to BigQuery

- Click the sidebar button to upload the logged data to Google BigQuery.

## Code Explanation

### `config.py`
- Loads BigQuery credentials.
- Defines exercise groups and exercises.

### `data.py`
- Saves workout data to a CSV file.
- Uploads data to BigQuery.

### `ui.py`
- Manages the user interface:
  - Home Page
  - Log Workout Page
  - View Progress Page

### `main.py`
- Initializes the app.
- Manages navigation between different pages.
- Handles data upload to BigQuery.