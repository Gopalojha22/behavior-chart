# Behavior Chart

A universal Flask web application that visualizes investment behavior and performance comparison through interactive charts. Upload your own CSV files or use the default datasets.

## Features

- **CSV File Upload**: Upload any two CSV files with historical data for comparison
- **SIP Performance Analysis**: Compare systematic investment plan (SIP) performance between any two datasets
- **Interactive Charts**: Dynamic visualization using Chart.js with smooth animations
- **Universal Format**: Works with any CSV files containing date and percentage change data
- **Default Datasets**: Includes Nifty 50 vs Nifty Next 50 comparison

## Installation

1. Clone the repository:
```bash
git clone https://github.com/OjhaGopal/behavior-chart.git
cd behavior-chart
```

2. Create and activate virtual environment:
```bash
python -m venv venv

# For Git Bash on Windows:
source venv/Scripts/activate

# Or navigate to Scripts directory:
cd venv/Scripts
```

3. Install dependencies:
```bash
# If virtual environment is activated:
pip install flask

# Or from Scripts directory:
cd venv/Scripts && pip install flask
```

## Usage

1. Run the application:
```bash
# Method 1: From Scripts directory
cd venv/Scripts && python ../../app.py

# Method 2: Activate environment first
source venv/Scripts/activate
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`
3. Upload two CSV files or view the chart with default data

## CSV File Format

Your CSV files should have the following format:
```
Date,Monthly Change %
01/01/2020,5.2
02/01/2020,-2.1
03/01/2020,3.8
```

- **Date**: MM/DD/YYYY format
- **Monthly Change %**: Percentage change for that month

## API Endpoints

- `/` - File upload page
- `/chart` - Interactive chart display
- `/upload` - Handle CSV file uploads
- `/data` - SIP performance data (from uploaded or default files)
- `/custom-data` - Custom dataset (SBIN vs FD comparison)

## Production Deployment

### Environment Variables
Copy `.env.example` to `.env` and set:
```
SECRET_KEY=your-random-secret-key
FLASK_ENV=production
PORT=5000
```

### Deploy to Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
heroku config:set SECRET_KEY=your-random-secret-key
heroku config:set FLASK_ENV=production
git push heroku main
```

### Run with Gunicorn (Production)
```bash
pip install -r requirements.txt
gunicorn app:app
```

## License

MIT License