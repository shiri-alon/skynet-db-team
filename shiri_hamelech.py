from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)





def create_connection():
    # Create a cursor object
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
    return conn

def execute_query(query="SELECT * FROM trial;"):
    # Create a connection and a cursor
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Get column names from cursor description
        column_names = [description[0] for description in cursor.description]

        # Convert each row into a dictionary with column names as keys
        results = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            results.append(row_dict)

        # Commit and close the connection
        conn.commit()
        conn.close()

        # Return the list of dictionaries (objects)
        return results
    except Exception as e:
        # Ensure the connection is closed in case of an error
        conn.close()
        raise e




# Route for the home page
@app.route('/')
def home():
    return "Welcome to the Flask server!"

# Route for the getAll API
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
        data = execute_query(query)
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
        data = execute_query(query)
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/getLaunchById', methods=['GET'])
def getLaunchById():
    # Get ID from query parameters
    launch_id = request.args.get('id')

    # Validate and sanitize input
    if not launch_id or not launch_id.isdigit():
        return jsonify({"error": "Invalid ID"}), 400
    
    # Prepare query
    query = f"SELECT * FROM launch WHERE launch_id = {launch_id}"
    
    # Fetch data
    try:
        data = execute_query(query)
        if data:
            return jsonify({"data": data[0]})
        else:
            return jsonify({"error": "No data found for the given ID"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#TODO:doing now
@app.route('/api/getCasualtyById', methods=['GET'])
def getCasualtyById():
    # Get ID from query parameters
    casualty_id = request.args.get('id')

    # Validate and sanitize input
    if not casualty_id or not casualty_id.isdigit():
        return jsonify({"error": "Invalid ID"}), 400
    
    # Prepare query
    query = f"SELECT * FROM casualty WHERE casualty_id = {casualty_id}"
    
    # Fetch data
    try:
        data = execute_query(query)
        if data:
            return jsonify({"data": data[0]})
        else:
            return jsonify({"error": "No data found for the given ID"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# #TODO
@app.route('/api/wasIntercepted', methods=['GET'])
def wasIntercepted():
    # Prepare query
    query = "SELECT was_intercepted, COUNT(*) FROM launch GROUP BY was_intercepted"
    
    # Fetch data
    try:
        data = execute_query(query)
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# #TODO
@app.route('/api/getLaunchByDate', methods=['GET'])
def getLaunchByDate():
    # Prepare query
    query = "SELECT start_date, COUNT(*) FROM launch GROUP BY start_date"
    
    # Fetch data
    try:
        data = execute_query(query)
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

