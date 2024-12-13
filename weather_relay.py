import json
import subprocess
import requests

# Define the web service endpoint
WEB_SERVICE_URL = "https://6883-190-210-38-133.ngrok-free.app/api/sensors"  # Replace with your actual web service URL

# Start rtl_433 process
process = subprocess.Popen(['rtl_433', '-F', 'json'], stdout=subprocess.PIPE)

# Read output line by line
for line in iter(process.stdout.readline, b''):
    try:
        # Decode the JSON output from rtl_433
        data = json.loads(line.decode('utf-8').strip())

        # Optionally, you can add custom processing here, for example, adjusting units
        # Example: converting temperature from tenths of a degree if needed
        data['temperature'] = data['temperature'] / 10 if 'temperature' in data else None

        # Send the JSON data to the web service via POST request
        response = requests.post(WEB_SERVICE_URL, json=data)

        # Check if the data was successfully sent
        if response.status_code == 200:
            print(f"Data successfully sent: {data}")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print(f"Response content: {response.content}")

    except json.JSONDecodeError:
        print("Received invalid JSON, skipping...")
    except requests.RequestException as e:
        print(f"Failed to send data due to network error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
