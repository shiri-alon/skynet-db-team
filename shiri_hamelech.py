from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)



DATABASE = 'defaultdb'
USER = 'avnadmin'
PASSWORD = 'AVNS_S8oDGGNacTWZPB-XVhR'
HOST = 'pg-2026da66-zr101-a12c.h.aivencloud.com'  # e.g., 'localhost'
PORT = '11302'  # e.g., '5432'


# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname=DATABASE,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)


def create_connection(query="SELECT * FROM trial;"):
    # Create a cursor object
    cursor = conn.cursor()

    # Define your query
    try:
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Print fetched rows
        for row in rows:
            print(row)
       
        return rows        
    except Exception as e:
        print(f"An error occurred: {e}")







# Route for the home page
@app.route('/')
def home():
    return "Welcome to the Flask server!"


@app.route('/api/getAll', methods=['GET'])
def getAll():
    # Get table name from query parameters
    table_name = request.args.get('table_name')
    # Sanitize table name to prevent SQL injection
    if not table_name or not table_name.isidentifier():
        return jsonify({"error": "Invalid table name"}), 400
    
    # Construct query
    query = f"SELECT * FROM {table_name}"
    
    # Fetch data
    try:
        data = create_connection(query)
        print(data)
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/getColumns', methods=['GET'])
def getColumns():
    # Get table name and column names from query parameters
    table_name = request.args.get('table_name')
    columns = request.args.get('columns')

    # Sanitize input
    if not table_name or not table_name.isidentifier() or not columns:
        return jsonify({"error": "Invalid table name or columns"}), 400
    
    # Prepare query
    columns_list = columns.split(',')
    columns_str = ', '.join([f'"{col.strip()}"' for col in columns_list])
    query = f"SELECT {columns_str} FROM {table_name}"
    
    # Fetch data
    try:
        data = create_connection(query)
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

