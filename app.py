import os
import cv2
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
    print("Successfully read image! Partitioning image...")
    rect_coords = partition(file.filename)

    root_name = file.filename.split(".")[0]
    result_dir = "processing/segmentation/results/{}/".format(root_name)
    allergies = request.form.get("allergies").split()

    final = cv2.imread(f, cv2.IMREAD_COLOR)

    print("Successfully partitioned image! Drawing image...")
    is_legal = True
    for i, rect_coord in enumerate(rect_coords):
        print("Started drawing rectangle: {}".format(i))
        lo_coord, hi_coord = rect_coord
        is_legal = check_image("{}{}.jpg".format(result_dir, i+1), allergies)

        if is_legal: color = (0,255,0)
        else: color = (0,0,255)
        cv2.rectangle(final, lo_coord, hi_coord, color, 2)
        print("Finished drawing rectangle: {}".format(i))

    cv2.imwrite("results/{}".format(file.filename), final)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
