import os
from flask import Flask, render_template, request

from processing.segmentation.partition import partition

app = Flask(__name__)

UPLOAD_FOLDER = "processing/segmentation/input/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    
    file.save(f)
    partition(file.filename)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)