"""
__name__ = partition.py
__authors__ = HackPrinceton 2017 Best Team
__description__ = File that partitions the image into bounding boxes
using OpenCV
"""

import numpy as np
import cv2
import copy

import settings as s

def process_image(img_name):
    img = cv2.imread(img_name, cv2.IMREAD_COLOR)
    dst = copy.deepcopy(img)
    rois_h = divideHW(dst, 1, s.THRESHOLD1, s.THRESHOLD2)

    print(rois_h)

    for i in range(len(rois_h)):
        if s.VERTICAL_DIVIDE:
            roi_h = dst[rois_h[i]]
            rois_w = divideHW(roi_h, 0, s.THRESHOLD1, s.THRESHOLD2)

            for j in range(len(rois_w)):
                rois_w[j][1] += rois_h[i][1]
                cv2.rectangle(dst, rois_w[j], (0, 255, 0), 1)
                # rois_w[j].x = rois_w[j].x * s.SCALE
                # rois_w[j].y = rois_w[j].y * s.SCALE
                # rois_w[j].width = rois_w[j].width * s.SCALE
                # rois_w[j].height = rois_w[j].height * s.SCALE
                # cv2.rectangle(dst, rois_w[j], (0, 255, 0), 3)
        cv2.rectangle(dst, rois_h[i], (0, 0, 255), 2)
        # rois_h[i].x = rois_h[i].x * s.SCALE
        # rois_h[i].y = rois_h[i].y * s.SCALE
        # rois_h[i].width = rois_h[i].width * s.SCALE
        # rois_h[i].height = rois_h[i].height * s.SCALE
        # cv2.rectangle(dst, rois_h[i], (0, 0, 255), 3)

    cv2.imwrite(s.OUTPUT_NAME, dst)

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
    reduced_img = cv2.reduce(gray_img, dim, cv2.REDUCE_AVG)
    canny_img   = cv2.Canny(reduced_img, threshold1, threshold2)
    pts = cv2.findNonZero(canny_img)

    rects = []
    rect = [0, 0, cols, rows] # x, y, width, height
    if pts.size > 0:
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

def main(img_name):
    """
    name of the iamge to be analyzed
    """
    process_image(img_name)

if __name__ == "__main__":
    main("test.jpg")