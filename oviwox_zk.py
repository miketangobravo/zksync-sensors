import json
import subprocess
import serial
import threading
import logging
from web3 import Web3
import os


# Set up logging to file
LOG_FILE = "/var/log/oviwox.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# zkSync configuration
ZKSYNC_RPC_URL = "https://zksync2-testnet.zksync.dev"  # zkSync testnet
CONTRACT_ADDRESS = "0x2B2CdB657138cB3F5381D8C482e72B2657A1256B"  # Replace with deployed contract address
PRIVATE_KEY = os.getenv("ZKSYNC_PRIVATE_KEY")

# Contract ABI
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "string", "name": "data", "type": "string"}],
        "name": "storeData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]

# Initialize Web3 connection
web3 = Web3(Web3.HTTPProvider(ZKSYNC_RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
logging.info(f"Connected to zkSync: {web3.isConnected()}")

def write_to_zksync(data):
    """Writes data to zkSync smart contract."""
    try:
        nonce = web3.eth.getTransactionCount(account.address)
        transaction = contract.functions.storeData(json.dumps(data)).buildTransaction({
            'chainId': web3.eth.chain_id,
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce
        })
        signed_tx = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        logging.info(f"Data written to zkSync. Tx hash: {web3.toHex(tx_hash)}")
    except Exception as e:
        logging.error(f"Error writing to zkSync: {e}")

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

            write_to_zksync(processed_data)
        except json.JSONDecodeError:
            logging.error("Invalid JSON from weather station.")
        except Exception as e:
            logging.error(f"Error in weather station relay: {e}")

# Function to handle Vinduino sensor data via serial
def vinduino_relay():
    # Open the serial connection to the Cypress dongle
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)  # Adjust baud rate as needed

    logging.info("Listening for Vinduino sensor data on /dev/ttyACM0...")

    # Continuously read from the serial port
    while True:
        if ser.in_waiting > 0:
            # Read a line of data from the serial port
            line = ser.readline().decode('utf-8').rstrip()
            logging.info(f"Received: {line}")

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
                write_to_zksync(data)
            except Exception as e:
                logging.error(f"Error parsing Vinduino data: {e}")

# Create threads for each function
# weather_thread = threading.Thread(target=weather_station_relay)
vinduino_thread = threading.Thread(target=vinduino_relay)

# Start the threads
#weather_thread.start()
vinduino_thread.start()

# Join the threads to keep the program running
#weather_thread.join()
vinduino_thread.join()

