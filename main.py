from datetime import datetime
import requests
import pandas as pd
import time  # Import time for introducing delay

# API endpoint
base_url = "https://data.cityofnewyork.us/resource/qgea-i56i.json"

# Initialize data list and offset
data = []
rows_per_request = 1000
offset = 0

# Calculate date 6 months ago in the correct format (including time)
six_months_ago = (datetime.now() - pd.DateOffset(months=18)).strftime("%Y-%m-%dT%H:%M:%S.000")

# Fetch data with pagination
while True:
    print(f"Fetching rows {offset} to {offset + rows_per_request}...")

    # Make the request with the offset
    response = requests.get(base_url, params={
        "$limit": rows_per_request,
        "$offset": offset,
        "$where": f"cmplnt_fr_dt >= '{six_months_ago}'"
    })
    
    if response.status_code == 200:
        chunk = response.json()
        print("chunkkkk",chunk)
        if not chunk:  # No more data to fetch, exit loop
            break
        data.extend(chunk)  # Add fetched data to list
        offset += rows_per_request  # Increment offset for next batch

        # Introduce a delay to prevent hitting rate limits
        time.sleep(1)  # Adjust sleep time if needed (e.g., 1 second)

    else:
        print(f"Error: {response.status_code} - {response.text}")
        break

# Convert data to DataFrame
df = pd.DataFrame(data)

# Display the first few rows
print(df.head())
