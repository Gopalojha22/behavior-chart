# Behavior Chart

A Flask web application that visualizes investment behavior and performance comparison between Nifty 50 and Nifty Next 50 indices through interactive charts.

## Features

- **SIP Performance Analysis**: Compare systematic investment plan (SIP) performance between Nifty 50 and Nifty Next 50
- **Interactive Charts**: Dynamic visualization using Chart.js
- **Historical Data**: Analysis based on real historical market data
- **Custom Dataset**: Additional comparison with SBIN vs Fixed Deposit returns

## Installation

1. Clone the repository:
```bash
git clone https://github.com/OjhaGopal/behavior-chart.git
cd behavior-chart
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

## Data Sources

- Nifty 50 Historical Data
- Nifty Next 50 Historical Data

## API Endpoints

- `/` - Main dashboard
- `/data` - SIP performance data (Nifty 50 vs Nifty Next 50)
- `/custom-data` - Custom dataset (SBIN vs FD comparison)

## License

MIT License