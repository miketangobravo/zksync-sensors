import serial
import json

# Open the serial connection to the Cypress dongle
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)  # Adjust baud rate as needed

print("Listening for Vinduino sensor data on /dev/ttyACM0...")

# Continuously read from the serial port
while True:
    if ser.in_waiting > 0:
        # Read a line of data from the serial port
        line = ser.readline().decode('utf-8').rstrip()
        print(f"Received: {line}")

        # Example: parse the data (ignoring the start/end of packet and vin_relh field)
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

            # Convert to JSON
            json_output = json.dumps(data, indent=4)
            print(f"JSON Output: {json_output}")
        except (IndexError, ValueError) as e:
            print(f"Error parsing data: {e}")


