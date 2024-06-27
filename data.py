# data.py
from google.cloud import bigquery
import os
import pandas as pd
from config import get_bigquery_client

def save_to_csv(rows, filename):
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False, mode='a', header=not os.path.exists(filename))

def upload_to_bigquery(client, table_id, csv_file):
    dataset_id = "fitness_logs"
    
    # Define the schema based on table name
    if 'bodymeasurements' in table_id:
        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("Date", "DATE"),
                bigquery.SchemaField("Weight", "FLOAT"),
                bigquery.SchemaField("Body Fat", "FLOAT"),
                bigquery.SchemaField("Chest", "FLOAT"),
                bigquery.SchemaField("Waist", "FLOAT"),
                bigquery.SchemaField("Hips", "FLOAT"),
            ],
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
        )
    elif 'cardio' in table_id:
        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("Date", "DATE"),
                bigquery.SchemaField("Exercise", "STRING"),
                bigquery.SchemaField("Time", "FLOAT"),
            ],
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
        )
    else:
        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("Date", "DATE"),
                bigquery.SchemaField("Exercise", "STRING"),
                bigquery.SchemaField("Sets", "INTEGER"),
                bigquery.SchemaField("Reps", "INTEGER"),
                bigquery.SchemaField("Weight", "FLOAT"),
            ],
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
        )
    
    table_id = f"{dataset_id}.{table_id}"
    with open(csv_file, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    job.result()  # Waits for the job to complete
    os.remove(csv_file)  # Remove the file after uploading
