
import psycopg2

DATABASE = 'defaultdb'
USER = 'avnadmin'
PASSWORD = 'AVNS_S8oDGGNacTWZPB-XVhR'
HOST = 'pg-28822bd-zr101-a12c.f.aivencloud.com'  # e.g., 'localhost'
PORT = '11302'  # e.g., '5432'

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname=DATABASE,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

# Create a cursor object
cursor = conn.cursor()

# Define your query
query = "SELECT * FROM trial;"

try:
    # Execute the query
    cursor.execute(query)
    
    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Print fetched rows
    for row in rows:
        print(row)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
