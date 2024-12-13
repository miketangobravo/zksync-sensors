# oviwox.py

`oviwox.py` is a Python script designed to process and record sensor data on a custom zkSync blockchain, OVchain. It facilitates decentralized storage of verifiable data, ensuring provenance and integrity for applications in IoT, agritech, and supply chain monitoring.

## Features
- Collects sensor data from devices.
- Writes data to OVchain, a custom zkSync blockchain.
- Provides decentralized and tamper-proof data storage.
- Supports logging and integration with other applications.

---

## Wine Analysis Example

The `oviwox.py` script can be used to store and manage verifiable records, such as the following wine analysis stored in `wine_sample.json`. This data showcases the chemical, physical, and sensory properties of a wine sample, verified for compliance and quality.

### Wine Analysis Data

The `wine_sample.json` file contains the following information:

```json
{
  "certificate_date": "2022-10-04",
  "sample_manifested": "Vino Varietal Tinto-Malbec-Verdot-Cabernet Sauvignon-2018",
  "sample_number": "60-967478-2022",
  "presented_on": "2022-10-04",
  "batch_volume_liters": 4988.00,
  "container_type": "Not specified",
  "owner": {
    "name": "CUCHILLAS DE LUNLUNTA S.A.",
    "code": "B73260"
  },
  "address": "MAZA S/N Mendoza - Maipú - Russell",
  "parameters": {
    "density_20C_g_per_ml": 0.9920,
    "alcohol_percent_vol_20C": 14.7,
    "dry_extract_g_per_l": 32.6,
    "reducing_sugars_g_per_l": 3.65,
    "total_acidity_tartaric_g_per_l": 4.74,
    "volatile_acidity_acetic_g_per_l": 0.75,
    "sulfates_SO4K2_g_per_l": "<1.00",
    "sorbic_acid_mg_per_l": "Not detected",
    "methanol_ml_per_l": "<0.51",
    "total_sulfur_dioxide_mg_per_l": 75,
    "polarimetric_deviation": "Not detected",
    "microscopic_observation": "Not detected"
  },
  "sensory_attributes": {
    "flavor": "Vinoso",
    "aroma": "Normal",
    "appearance": "Limpid",
    "color": "Tinto"
  },
  "metals_content_mg_per_l": {
    "copper": "<1.00",
    "lead": "<0.10",
    "cadmium": "<0.01",
    "arsenic": "<0.20",
    "zinc": "<5.00"
  },
  "observations": "Analysis M-1741170 (142 Lts), M-1830008 (4846 Lts). Property of Organic Costaflores Sociedad Anonima. CUIT: 30-71099828-7",
  "classification": [
    "Libre Circulación",
    "Vino Genuino",
    "Apto para el Consumo"
  ]
}
```

This analysis provides a comprehensive overview of the wine’s properties, including:
- **Physical properties** (e.g., density, alcohol content).
- **Chemical properties** (e.g., acidity, sulfates, methanol).
- **Sensory evaluation** (e.g., flavor, aroma, appearance).
- **Metal content** (e.g., copper, lead, cadmium).

### Use Case
With `oviwox.py`, this data can be stored on OVchain to provide:
- Immutable records for regulatory compliance.
- Transparent quality assurance for consumers.
- Decentralized storage for provenance tracking.

---

## Getting Started

### Prerequisites
- Python 3.8+
- Dependencies specified in `requirements.txt`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/miketangobravo/zksync-sensors.git
   cd zksync-sensors
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
Run the script to process and store data:

```bash
python oviwox.py
```

### Configuration
Edit the configuration file to specify:
- Blockchain endpoint.
- Sensor data sources.
- Logging preferences.

---

## License
This project is licensed under the MIT License.

---

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

---

## Contact
For more information, reach out to:
- **Author:** Mike Tango Bravo
- **Email:** [nft@openvino.org](mailto:nft@openvino.org)


