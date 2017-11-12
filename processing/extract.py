import io
from google.cloud import vision

"""
_name_ = extract.py
_authors_ = HackPrinceton 2017 Best Team
_description_ = File that extracts logos and web descriptions of an image using Google Vision
"""

# prints the web descriptions
# taken from https://cloud.google.com/vision/docs/internet-detection
def report(annotations):
    """Prints detected features in the provided web annotations."""
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if annotations.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        print ('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))

# given a file path, returns logos and web descriptions (if any)
def get_logos_web(filename):
    
    vision_client = vision.Client()
    
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(content=content)
        
    logos = image.detect_logos()
    web = image.detect_web()

    return((logos,web))
