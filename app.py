from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import csv
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_csv_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)
            return headers, rows
    except Exception:
        return [], []

def parse_date_value(date_str):
    date_formats = ['%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d', '%Y']
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).year
        except ValueError:
            continue
    
    try:
        return int(date_str.strip()[:4])
    except:
        return None

def process_uploaded_data(file1_path, file2_path, config):
    try:
        headers1, rows1 = load_csv_data(file1_path)
        headers2, rows2 = load_csv_data(file2_path)
        
        if not headers1 or not headers2:
            return None
        
        x_idx1 = headers1.index(config['file1_x_field'])
        y_idx1 = headers1.index(config['file1_y_field'])
        x_idx2 = headers2.index(config['file2_x_field'])
        y_idx2 = headers2.index(config['file2_y_field'])
        
        data1, data2, labels = [], [], []
        
        for row in rows1:
            if len(row) > max(x_idx1, y_idx1):
                try:
                    x_val = row[x_idx1].strip()
                    y_val = float(row[y_idx1].strip())
                    
                    year = parse_date_value(x_val)
                    if not year:
                        year = len(data1) + 1
                    
                    data1.append(y_val)
                    labels.append(year)
                except (ValueError, IndexError):
                    continue
        
        for row in rows2:
            if len(row) > max(x_idx2, y_idx2):
                try:
                    y_val = float(row[y_idx2].strip())
                    data2.append(y_val)
                except (ValueError, IndexError):
                    continue
        
        min_length = min(len(data1), len(data2), len(labels))
        
        return {
            'labels': labels[:min_length],
            'dataset1': data1[:min_length],
            'dataset2': data2[:min_length],
            'dataset1_name': config.get('file1_display_name', 'Dataset 1'),
            'dataset2_name': config.get('file2_display_name', 'Dataset 2'),
            'color1': config.get('color1', '#0066cc'),
            'color2': config.get('color2', '#00cc66')
        }
        
    except Exception:
        return None

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        return redirect(url_for('upload_page'))
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    if file1.filename == '' or file2.filename == '':
        return redirect(url_for('upload_page'))
    
    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        
        try:
            file1.save(filepath1)
            file2.save(filepath2)
        except (OSError, IOError):
            return redirect(url_for('upload_page'))
        
        session['uploaded_files'] = {
            'file1': filepath1,
            'file2': filepath2
        }
        
        return redirect(url_for('field_selector'))
    
    return redirect(url_for('upload_page'))

@app.route('/field-selector')
def field_selector():
    if 'uploaded_files' not in session:
        return redirect(url_for('upload_page'))
    
    files = session['uploaded_files']
    headers1, _ = load_csv_data(files['file1'])
    headers2, _ = load_csv_data(files['file2'])
    
    if not headers1 or not headers2:
        return redirect(url_for('upload_page'))
    
    return render_template('field_selector.html', 
                         headers1=headers1, 
                         headers2=headers2,
                         file1_name=os.path.basename(files['file1']),
                         file2_name=os.path.basename(files['file2']))

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'uploaded_files' not in session:
        return redirect(url_for('upload_page'))
    
    required_fields = ['file1_x_field', 'file1_y_field', 'file2_x_field', 'file2_y_field']
    for field in required_fields:
        if field not in request.form or not request.form[field]:
            return redirect(url_for('field_selector'))
    
    session['field_config'] = {
        'file1_x_field': request.form['file1_x_field'],
        'file1_y_field': request.form['file1_y_field'],
        'file2_x_field': request.form['file2_x_field'],
        'file2_y_field': request.form['file2_y_field'],
        'file1_display_name': request.form.get('file1_display_name', 'Dataset 1'),
        'file2_display_name': request.form.get('file2_display_name', 'Dataset 2'),
        'color1': request.form.get('color1', '#0066cc'),
        'color2': request.form.get('color2', '#00cc66')
    }
    
    return redirect(url_for('chart'))

@app.route('/chart')
def chart():
    return render_template('index.html')

@app.route('/data')
def get_data():
    # Always return valid JSON, never HTML
    try:
        if 'uploaded_files' in session and 'field_config' in session:
            files = session['uploaded_files']
            config = session['field_config']
            
            if os.path.exists(files['file1']) and os.path.exists(files['file2']):
                processed_data = process_uploaded_data(files['file1'], files['file2'], config)
                if processed_data:
                    return jsonify(processed_data)
        
        # Default data
        years = list(range(2010, 2025))
        return jsonify({
            'labels': years,
            'dataset1': [1000 * (1.12 ** i) for i in range(len(years))],
            'dataset2': [1000 * (1.15 ** i) for i in range(len(years))],
            'dataset1_name': 'Nifty 50',
            'dataset2_name': 'Nifty Next 50',
            'color1': '#0066cc',
            'color2': '#00cc66'
        })
    except:
        # Fallback data - always return JSON
        years = list(range(2010, 2025))
        return jsonify({
            'labels': years,
            'dataset1': [1000 * (1.12 ** i) for i in range(len(years))],
            'dataset2': [1000 * (1.15 ** i) for i in range(len(years))],
            'dataset1_name': 'Sample Dataset 1',
            'dataset2_name': 'Sample Dataset 2',
            'color1': '#0066cc',
            'color2': '#00cc66'
        })



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)