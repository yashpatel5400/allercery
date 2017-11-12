"""
__name__ = partition.py
__authors__ = HackPrinceton 2017 Best Team
__description__ = File that partitions the image into bounding boxes
using OpenCV
"""

import numpy as np
import cv2
import copy
import os

import processing.segmentation.settings as s
# from processing.segmentation.hed import segment_edges

def partition_image(img_name):
    img_root = img_name.split(".")[0]

    # orig = cv2.imread("{}{}".format(s.INPUT_DIR, img_name), cv2.IMREAD_COLOR)
    dst  = cv2.imread("{}{}".format(s.INPUT_DIR, img_name), cv2.IMREAD_COLOR)

    rois_h = divideHW(dst, 1, s.THRESHOLD1, s.THRESHOLD2)
    rect_count = 0

    dir_name = "{}{}/".format(s.PARTITION_OUTPUT_DIR, img_root)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    rect_coords = []
    if rois_h is not None:
        print("Analyzed rectangles! Found: {}".format(len(rois_h)))
        for i in range(len(rois_h)):
            if s.VERTICAL_DIVIDE:
                roi_h  = dst[
                            rois_h[i][1]:(rois_h[i][1] + rois_h[i][3]), 
                            rois_h[i][0]:(rois_h[i][0] + rois_h[i][2]), 
                            :
                        ]
                rois_w = divideHW(roi_h, 0, s.THRESHOLD1, s.THRESHOLD2)

                if rois_w is not None:
                    for j in range(len(rois_w)):
                        rois_w[j][1] += rois_h[i][1]

                        x, y, width, height = rois_w[j]
                        if width > s.DIM_THRESHOLD and height > s.DIM_THRESHOLD:
                            rect_count += 1

                            rect_coords.append([(x, y), (x + width, y + height)])
                            cv2.imwrite("{}{}.jpg".format(dir_name, rect_count), 
                                dst[y:(y + height), x:(x + width), :])
            print("Partitioned rectangle {}".format(i))
    return rect_coords

def divideHW(img, dim, threshold1, threshold2):
    """
    helper function returns rectangles according horizontal or vertical projection of given image
    parameters:
    src (Mat) : source image
    dim (int) : dimension 1 for horizontal 0 for vertical projection
    threshold1 (float) : first threshold for the hysteresis procedure ( used by internal Canny )
    threshold2 (float) : second threshold for the hysteresis procedure ( used by internal Canny )
    """
    rows, cols, colors = img.shape # separated for sake of clarity
    gray_img    = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    reduced_img = cv2.reduce(gray_img, dim, 1) #cv2.REDUCE_AVG)
    canny_img   = cv2.Canny(reduced_img, threshold1, threshold2)
    pts = cv2.findNonZero(canny_img)

    rects = []
    rect = [0, 0, cols, rows] # x, y, width, height
    if pts is None:
        return

    rects.append(rect)
    ref_x = 0
    ref_y = 0

    for i in range(len(pts)):
        x, y = pts[i][0]
        rect = copy.deepcopy(rect)
        if dim:
            rect[3] = y - ref_y
            rects.append(rect)
            rect[1] = y
            ref_y = rect[1]
            if i == len(pts) - 1:
                rect[3] = rows - y
                rects.append(rect)
        else:
            rect[2] = x - ref_x
            rects.append(rect)
            rect[0] = x
            ref_x = rect[0]
            if i == len(pts) - 1:
                rect[2] = cols - x
                rects.append(rect)
    return rects

def partition(img_name):
    """
    name of the iamge to be analyzed
    """
    # segment_edges([img_name])
    return partition_image(img_name)

if __name__ == "__main__":
    partition("cereal.jpg")
