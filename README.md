# OpenVino sensor data logger to zkSync

## Overview
The `oviwox_zk.py` application is a Python-based script designed to read sensor data, process it, and securely log it on the zkSync blockchain. It integrates multiple data sources, from a weather station and vinduino soil moisture sensors, and writes them to a smart contract deployed on zkSync.

---

## Features
- **Real-time Sensor Data Capture**:
  - Reads data from Vinduino sensors over LoRa.
  - Processes weather station data via `rtl_433`.
- **Blockchain Integration**:
  - Logs processed sensor data into a smart contract on zkSync.
  - Ensures data immutability and transparency.
- **Error Handling**:
  - Logs all errors and exceptions for easy debugging.
  - Handles invalid or malformed data gracefully.
- **Configurable Logging**:
  - Logs all activity to `/var/log/oviwox.log`.

---

## Requirements

### Software
- Python 3.8+
- Libraries:
  - `web3`
  - `serial`
  - `json`
  - `subprocess`
  - `threading`
  - `dotenv`

### Hardware
- **Vinduino Sensor** connected via a LoRa dongle connected to a USB port (`/dev/ttyACM0`).
- **RTL-SDR Dongle** for weather station data capture (optional).

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/oviwox.git
cd oviwox
```

### 2. Install Dependencies
Create a virtual environment and install required Python libraries:
```bash
python3 -m venv env
source env/bin/activate
pip install web3 pyserial python-dotenv
```

### 3. Configure Environment Variables
Create a `.env` file in the project directory and populate it with your private key:
```plaintext
ZKSYNC_PRIVATE_KEY=your_private_key_here
ZKSYNC_RPC_URL=https://sepolia.era.zksync.dev
```

### 4. Deploy or Update the Smart Contract
Ensure the smart contract is deployed on zkSync and note its address. Update the `CONTRACT_ADDRESS` in the script accordingly.

---

## Usage

### 1. Start the Application
Run the script to start reading and logging sensor data:
```bash
python3 oviwox_zk.py
```

### 2. Monitor Logs
Check logs for activity or errors:
```bash
tail -f /var/log/oviwox.log
```

---

## Data Flow
1. **Input**: Captures data from:
   - Vinduino sensors (via serial input).
   - Weather stations (via RTL-SDR).
2. **Processing**:
   - Formats sensor data into JSON.
   - Validates and handles malformed or incomplete data.
3. **Output**:
   - Writes data to the zkSync blockchain.

---

## Troubleshooting

### Insufficient Funds
Ensure your zkSync wallet has sufficient testnet ETH for gas fees. Use the Sepolia Testnet faucet to acquire funds.

### Not Authorized Error
Check if your wallet is authorized in the deployed contract. If not, redeploy the contract or update the authorization list (requires access to the owner account).

---

## Smart Contract

### Overview of the Smart Contract
The smart contract used by `oviwox_zk.py` is called `OpenVino_oviwox`. It is responsible for securely storing sensor data on the blockchain. Key features include:

- **Owner Authorization**: Only the contract owner can manage authorized updaters.
- **Updater Management**:
  - Allows authorized addresses to store data.
  - Supports revoking updater permissions.
- **Data Storage**:
  - Stores data with a timestamp and tracks the updater's address.
  - Emits events for each data entry.
- **Access Functions**:
  - View stored data by ID.
  - Retrieve all stored data.


### Deploying the Smart Contract with Remix
1. **Open Remix**:
   - Navigate to [Remix IDE](https://remix.ethereum.org/).

2. **Create a New File**:
   - In the File Explorer, create a new file (e.g., `OpenVino_oviwox.sol`).
   - Paste the smart contract code into this file.

3. **Compile the Contract**:
   - Go to the **Solidity Compiler** tab.
   - Select a compatible compiler version (e.g., `0.8.20`).
   - Click **Compile IotStoreData.sol**.

4. **Deploy the Contract**:
   - Go to the **Deploy & Run Transactions** tab.
   - Set **Environment** to **Injected Web3** to connect MetaMask.
   - Ensure MetaMask is set to the zkSync Sepolia Testnet.
   - Click **Deploy** next to `OpenVino_oviwox`.

5. **Confirm the Deployment**:
   - Approve the transaction in MetaMask.
   - Note the contract address displayed in Remix.

6. **Interact with the Contract**:
   - Use the **Deployed Contracts** section in Remix to call functions like `authorizeUpdater` and `storeData`.

---

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a detailed description.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.


