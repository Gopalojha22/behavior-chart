from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/field-selector')
def field_selector():
    return render_template('field_selector.html')

@app.route('/chart')
def chart():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)