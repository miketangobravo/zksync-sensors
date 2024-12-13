import json
import subprocess
import requests
import serial
import threading

# Define the web service endpoint
WEB_SERVICE_URL = "https://6883-190-210-38-133.ngrok-free.app/api/sensors"  # Replace with your actual web service URL

# Function to handle weather station data via rtl_433
def weather_station_relay():
    # Start rtl_433 process
    process = subprocess.Popen(['rtl_433', '-F', 'json'], stdout=subprocess.PIPE)

    # Read output line by line
    for line in iter(process.stdout.readline, b''):
        try:
            # Decode the JSON output from rtl_433
            data = json.loads(line.decode('utf-8').strip())

            # Extract and process the required fields
            processed_data = {
                "wx_batterylow": data.get('batterylow'),  # Output as wx_batterylow
                "avewindspeed": round(data.get('avewindspeed', 0) * 0.539957, 2),  # Convert from kph to knots
                "gustwindspeed": round(data.get('gustwindspeed', 0) * 0.539957, 2),  # Convert from kph to knots
                "winddirection": data.get('winddirection'),  # Keep as is
                "cumulativerain": data.get('cumulativerain'),  # Keep as is
                "temperature": data.get('temperature'),  # Keep as is
                "humidity": data.get('humidity'),  # Keep as is
                "light": data.get('light'),  # Keep as is
                "uv": data.get('uv')  # Keep as is
            }

            # Send the filtered and processed JSON data to the web service via POST request
            response = requests.post(WEB_SERVICE_URL, json=processed_data)

            # Check if the data was successfully sent
            if response.status_code == 200:
                print(f"Weather data successfully sent: {processed_data}")
            else:
                print(f"Failed to send weather data. Status code: {response.status_code}")
                print(f"Response content: {response.content}")

        except json.JSONDecodeError:
            print("Received invalid JSON from weather station, skipping...")
        except requests.RequestException as e:
            print(f"Failed to send weather data due to network error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while sending weather data: {e}")

# Function to handle Vinduino sensor data via serial
def vinduino_relay():
    # Open the serial connection to the Cypress dongle
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)  # Adjust baud rate as needed

    print("Listening for Vinduino sensor data on /dev/ttyACM0...")

    # Continuously read from the serial port
    while True:
        if ser.in_waiting > 0:
            # Read a line of data from the serial port
            line = ser.readline().decode('utf-8').rstrip()
            print(f"Received: {line}")

            # Parse the Vinduino sensor data
            try:
                # Remove starting and ending characters (like $, !) if needed
                if line.startswith('$') and line.endswith('!'):
                    line = line[1:-1]

                # Split the data into parts by commas
                parts = line.split(',')

                # Construct the JSON object with meaningful field names
                data = {
                    "vinduino_id": parts[1],  # Vinduino sensor ID
                    "0.05m": float(parts[2]),  # Sensor at 0.05 meters
                    "0.5m": float(parts[3]),   # Sensor at 0.5 meters
                    "1m": float(parts[4]),     # Sensor at 1 meter
                    "2m": float(parts[5]),     # Sensor at 2 meters
                    "vin_bat": float(parts[6]),  # Battery voltage
                    "vin_temp": float(parts[7])  # Temperature (VIN)
                }

                # Convert to JSON and print it for debugging
                json_output = json.dumps(data, indent=4)
                print(f"JSON Output (Vinduino): {json_output}")

                # Send the JSON data to the web service via POST request
                response = requests.post(WEB_SERVICE_URL, json=data)

                # Check if the data was successfully sent
                if response.status_code == 200:
                    print(f"Vinduino data successfully sent: {data}")
                else:
                    print(f"Failed to send Vinduino data. Status code: {response.status_code}")
                    print(f"Response content: {response.content}")

            except (IndexError, ValueError) as e:
                print(f"Error parsing Vinduino data: {e}")
            except requests.RequestException as e:
                print(f"Failed to send Vinduino data due to network error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while sending Vinduino data: {e}")

# Create threads for each function
weather_thread = threading.Thread(target=weather_station_relay)
vinduino_thread = threading.Thread(target=vinduino_relay)

# Start the threads
weather_thread.start()
vinduino_thread.start()

# Join the threads to keep the program running
weather_thread.join()
vinduino_thread.join()

