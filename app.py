import os
import cv2
from flask import Flask, render_template, request
import time

import io
from google.cloud import vision

from processing.segmentation.partition import partition
from processing.extraction.map_ingredients import make_table
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
    allergies = set([allergy.strip() for allergy in request.form.get("allergies").split(",")])
    final = cv2.imread(f, cv2.IMREAD_COLOR)

    print("Successfully partitioned image! Drawing {} rectangles...".format(len(rect_coords)))
    is_legal = True

    vision_client = vision.Client()
    ingredient_map = make_table("processing/extraction/cereal_ingredients.csv")
    print(ingredient_map.keys())

    for i, rect_coord in enumerate(rect_coords):
        lo_coord, hi_coord = rect_coord
        
        try:
            print("Started drawing rectangle: {}".format(i))

            filename = "{}{}.jpg".format(result_dir, i+1)
            with io.open(filename, 'rb') as image_file:
                content = image_file.read()
                image = vision_client.image(content=content)

            web = image.detect_web()
            entities = [x.description for x in web.web_entities]

            is_legal = True
            for entity in entities:
                if entity in ingredient_map:
                    for ingredient in ingredient_map[entity]:
                        if ingredient.lower() in allergies:
                            is_legal = False
                            break

                for ingredient in entity.split():
                    if ingredient.lower() in allergies:
                        is_legal = False
                        break

            print("Got {} for rect {}".format(is_legal, i))

            if is_legal == 1: color = (0,255,0)
            else: color = (0,0,255)
        except:
            print("Timed out for rect {}".format(i))
            print("=====================================")
            continue

        cv2.rectangle(final, lo_coord, hi_coord, color, 2)
        print("Finished drawing rectangle: {}".format(i))
        print("=====================================")

    cv2.imwrite("results/{}".format(file.filename), final)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)