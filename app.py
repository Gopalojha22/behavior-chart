from flask import Flask, render_template, jsonify, request, redirect, url_for
import csv
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist (skip in serverless)
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
except:
    pass

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_monthly_changes(filename):
    """Reads monthly % change from CSV, returns (dates, changes) oldest-first."""
    dates = []
    changes = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) < 2:
                continue
            date_str = row[0].strip()
            change_str = row[1].strip()
            if not change_str:
                continue
            try:
                change = float(change_str) / 100.0  # convert % to decimal
            except ValueError:
                continue
            dates.append(date_str)
            changes.append(change)
    # Reverse order so oldest month first
    dates.reverse()
    changes.reverse()
    return dates, changes

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/chart')
def chart():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        return redirect(url_for('index'))
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    if file1.filename == '' or file2.filename == '':
        return redirect(url_for('index'))
    
    if file1 and file2 and allowed_file(file1.filename) and allowed_file(file2.filename):
        # Get user-provided names (sanitized)
        name1 = request.form.get('name1', 'Dataset 1')[:50]  # Limit length
        name2 = request.form.get('name2', 'Dataset 2')[:50]  # Limit length
        
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], 'dataset1.csv')
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], 'dataset2.csv')
        names_file = os.path.join(app.config['UPLOAD_FOLDER'], 'names.txt')
        
        try:
            file1.save(filepath1)
            file2.save(filepath2)
            
            # Save the original names
            with open(names_file, 'w') as f:
                f.write(f"{name1}\n{name2}")
            
            return redirect(url_for('chart'))
        except:
            # If file operations fail (like in serverless), redirect to default chart
            return redirect(url_for('chart'))

@app.route('/custom-data')
def custom_data():
    # Custom dataset
    years = [
        2015, 2016, 2017, 2018, 2019,
        2020, 2021, 2022, 2023, 2024, 2025
    ]
    sbin_values = [
        10000.00, 8098.40, 10030.75, 9577.60, 10802.72,
        8899.50, 14903.71, 19864.06, 20781.68, 25730.70, 27130.60
    ]
    fd_values = [
        10000.00, 10700.00, 11449.00, 12250.43, 13107.96,
        14025.52, 15007.30, 16057.81, 17181.86, 18384.59, 19671.51
    ]

    return jsonify({
        "labels": years,
        "dataset1": sbin_values,
        "dataset2": fd_values,
        "dataset1_name": "SBIN",
        "dataset2_name": "Fixed Deposit"
    })

@app.route('/data')
def data():
    sip_amount = 1000
    sip_at_start = True  # True = invest at start of month, False = invest at end

    # Try to load uploaded files first, fallback to default files
    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'dataset1.csv')
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'dataset2.csv')
    
    try:
        if os.path.exists(file1_path) and os.path.exists(file2_path):
            dates_nifty50, nifty50_changes = load_monthly_changes(file1_path)
            dates_next50, next50_changes = load_monthly_changes(file2_path)
        else:
            # Fallback to default files
            dates_nifty50, nifty50_changes = load_monthly_changes(
                "Nifty 50 Historical Data (1) - Nifty 50 Historical Data (1).csv"
            )
            dates_next50, next50_changes = load_monthly_changes(
                "Nifty Next 50 Historical Data - Nifty Next 50 Historical Data.csv"
            )
    except:
        # If files don't exist, use fallback
        try:
            dates_nifty50, nifty50_changes = load_monthly_changes(
                "Nifty 50 Historical Data (1) - Nifty 50 Historical Data (1).csv"
            )
            dates_next50, next50_changes = load_monthly_changes(
                "Nifty Next 50 Historical Data - Nifty Next 50 Historical Data.csv"
            )
        except:
            # Return empty data if no files found
            return jsonify({
                "labels": [],
                "dataset1": [],
                "dataset2": [],
                "dataset1_name": "No Data",
                "dataset2_name": "No Data"
            })

    months = min(len(nifty50_changes), len(next50_changes))

    value_nifty50 = 0.0
    value_next50 = 0.0

    labels = []
    nifty50_values = []
    next50_values = []

    for i in range(months):
        # Format label from date
        try:
            dt = datetime.strptime(dates_nifty50[i], "%m/%d/%Y")
            label = dt.strftime("%m-%Y")
        except ValueError:
            label = dates_nifty50[i]
        labels.append(label)

        r_n = nifty50_changes[i]
        r_x = next50_changes[i]

        if sip_at_start:
            value_nifty50 = (value_nifty50 + sip_amount) * (1 + r_n)
            value_next50  = (value_next50 + sip_amount) * (1 + r_x)
        else:
            value_nifty50 = value_nifty50 * (1 + r_n) + sip_amount
            value_next50  = value_next50 * (1 + r_x) + sip_amount

        nifty50_values.append(round(value_nifty50, 2))
        next50_values.append(round(value_next50, 2))

    # Get dataset names from stored filenames
    dataset1_name = "Dataset 1"
    dataset2_name = "Dataset 2"
    names_file = os.path.join(app.config['UPLOAD_FOLDER'], 'names.txt')
    
    try:
        if os.path.exists(file1_path) and os.path.exists(file2_path) and os.path.exists(names_file):
            # Read stored original filenames
            with open(names_file, 'r') as f:
                lines = f.read().strip().split('\n')
                if len(lines) >= 2:
                    dataset1_name = lines[0]
                    dataset2_name = lines[1]
        elif not os.path.exists(file1_path) or not os.path.exists(file2_path):
            dataset1_name = "Nifty 50"
            dataset2_name = "Nifty Next 50"
    except:
        dataset1_name = "Nifty 50"
        dataset2_name = "Nifty Next 50"
    
    return jsonify({
        "labels": labels,
        "dataset1": nifty50_values,
        "dataset2": next50_values,
        "dataset1_name": dataset1_name,
        "dataset2_name": dataset2_name
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
