import json

json_data_launch = []
json_data_casualty = []

# Read json file and save information
with open("data.json", 'r') as f:
    json_data = json.load(f)
    for entry in json_data:
        if entry == "casualty":
            json_data_casualty.append(json_data)
        else:
            json_data_launch.append(entry)

print(json_data_casualty)
print(json_data_launch)

queries = []
for entry in json_data_launch:
    keys = tuple(entry.keys())
    values = tuple(entry.values())

    keys_as_s = str(keys).replace("'", "")

    # Define your query
    query = f"INSERT INTO casualty {keys_as_s} \
            VALUES {values}"
    queries.append(query)

print(queries)
