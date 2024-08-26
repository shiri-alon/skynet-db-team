
import psycopg2
import json
import requests
import flask
import time

DATABASE = 'defaultdb'
USER = 'avnadmin'
PASSWORD = 'AVNS_S8oDGGNacTWZPB-XVhR'
HOST = 'pg-2026da66-zr101-a12c.h.aivencloud.com'  # e.g., 'localhost'
PORT = '11302'  # e.g., '5432'
URL = "https://skynetgroup5.onrender.com/launch/historical"



def insert_to_db(json_data):

    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

    # Parsing casualty object from main object
    json_data_casualty = json_data.pop('casualty')
    # Add casualty id to json
    json_data['casualty_id'] = json_data_casualty['casualty_id']

    # Pop start and end point from json and add them seperately
    start_location, end_location = json_data.pop('start_location'), json_data.pop('end_location')

    json_data['start_location_x'] = start_location['x']
    json_data['start_location_y'] = start_location['y']
    json_data['end_location_x'] = end_location['x']
    json_data['end_location_y'] = end_location['y']

    # Parse between keys and values of each table
    keys_c = tuple(json_data_casualty.keys())
    values_c = tuple(json_data_casualty.values())
    keys_l = tuple(json_data.keys())
    values_l = tuple(json_data.values())


    # Drop ' from keys for each table
    keys_c_as_s = str(keys_c).replace("'", "")
    keys_l_as_s = str(keys_l).replace("'", "")

    # Define your queries
    query_c = f"INSERT INTO casualty {keys_c_as_s} \
                VALUES {values_c}"

    query_l = f"INSERT INTO launch {keys_l_as_s} \
                VALUES {values_l}"


    try:
        # Execute the queries
        # Create a cursor object, send queries and close
        cursor = conn.cursor()
        cursor.execute(query_c)
        cursor.execute(query_l)
        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Print fetched rows
        for row in rows:
            print(row)

        cursor.close()
        # commit
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        conn.commit()
        conn.close()

    # Seperate casualty from json

def handle_req_and_insert():
    try:
        # Read json file and save information
        response = requests.get(URL)

        response.raise_for_status()

        json_obj = response.json()
        print(json_obj)

        for entry in json_obj:
            insert_to_db(entry) 
    except requests.RequestException as e:
        print("An error occurred:", e)

# Main loop
while True:
    try:
        handle_req_and_insert()
        time.sleep(30)
    except KeyboardInterrupt:
        print("Script interrupted by user.")

