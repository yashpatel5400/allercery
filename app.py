import os
from flask import Flask, render_template, request

from processing.segmentation.partition import partition
from processing.extraction.check_image import check_image

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

    root_name = file.filename.split(".")[0]
    result_dir = "processing/segmentation/results/{}/".format(root_name)
    allergies = request.form.get("allergies").split()

    fits_allergy = {}
    for result in os.listdir(result_dir):
        fits_allergy[result] = check_image("{}{}".format(result_dir, result), allergies)
    print(fits_allergy)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)