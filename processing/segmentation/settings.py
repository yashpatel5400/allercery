"""
__author__ = HackPrinceton 2017 Best Team
__description__ = Global variable declarations (module-level) for partitioning
"""

# -------------------- Input Img Global Variables ---------------------------#
# training images split (in corresponding input directory)
TRAIN = 'train/'

# test images split (in corresponding input directory)
TEST = 'test/'

# -------------------- Input Directory Global Variables ---------------------#
# raw images and matrix files
INPUT_DIR = './input/'

# -------------------- Pre-trained Model Variables ---------------------------#
# website where the pre-trained model can be downloaded
MODEL_SITE = 'http://vcl.ucsd.edu/hed/hed_pretrained_bsds.caffemodel'

# metadata about the model needed to load pretrained Caffe models
MODEL_META = "deploy.prototxt"

# cached model filename
MODEL_FILENAME = "hed_pretrained_bsds.caffemodel"

# directory for models cache
MODEL_CACHE = "./cache/"

# -------------------- Output Directory Variables ---------------------------  #
# directory for final output images
OUTPUT_DIR = "./results/"

# --------------------- Overall Window ------------------------ #
WINDOW_NAME = "result"
OUTPUT_NAME = "result"

# --------------------- Overall Partitioning Parameters --------------------- #
SCALE = 4
VERTICAL_DIVIDE = 1

# thresholds for Canny edge detector
THRESHOLD1 = 0
THRESHOLD2 = 300

# threshold of how large a "slice" of the image must be to be considered
# a legal cut
DIM_THRESHOLD = 10