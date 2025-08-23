from flask import Flask, render_template, jsonify
import os

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/chart')
def chart():
    return render_template('index.html')

@app.route('/data')
def get_data():
    # Always return sample data for serverless
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

if __name__ == '__main__':
    app.run()