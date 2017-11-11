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

def process_image( int, void* ):
	dst = copy.deepcopy(src)
    vector<Rect> rois_h = divideHW( dst_resized, 1, s.THRESHOLD1, s.THRESHOLD2 )

    for( size_t i=0 i< rois_h.size() i++ )
    {
        if( s.VERTICAL_DIVIDE )
        {
            Mat roi_h = dst_resized( rois_h[i])

            vector<Rect> rois_w = divideHW( roi_h, 0, s.THRESHOLD1, s.THRESHOLD2 )

            for( size_t j=0 j< rois_w.size() j++ )
            {
                rois_w[j].y += rois_h[i].y
                rectangle( dst_resized, rois_w[j], Scalar( 0, 255, 0 ), 1 )
                rois_w[j].x = rois_w[j].x * s.SCALE
                rois_w[j].y = rois_w[j].y * s.SCALE
                rois_w[j].width = rois_w[j].width * s.SCALE
                rois_w[j].height = rois_w[j].height * s.SCALE

                rectangle( dst, rois_w[j], Scalar( 0, 255, 0 ), 3 )
            }
        }
        rectangle( dst_resized, rois_h[i], Scalar( 0, 0, 255 ), 2 )
        rois_h[i].x = rois_h[i].x * s.SCALE
        rois_h[i].y = rois_h[i].y * s.SCALE
        rois_h[i].width = rois_h[i].width * s.SCALE
        rois_h[i].height = rois_h[i].height * s.SCALE
        rectangle( dst, rois_h[i], Scalar( 0, 0, 255), 3 )
    }

    imshow( "resized", dst_resized )
    imshow( window_name, dst )
}

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
    rect = np.zeros((rows, cols))
    if pts.size > 0:
        rects.append(rect)

    ref_x = 0
    ref_y = 0

    for i in range(pts.size):
    	x, y = pts[i][0]
        if dim:
            rect.height = y - ref_y
            rects.push_back(rect)
            rect.y = y
            ref_y = rect.y
            if i == pts.size - 1:
                rect.height = gray.rows - y
                rects.push_back( rect )
        else:
            rect.width = x - ref_x
            rects.push_back(rect)
            rect.x = x
            ref_x = rect.x
            if i == pts.size - 1:
                rect.width = gray.cols - x
                rects.push_back(rect)
    return rects

def main(img_name):
	"""
	name of the iamge to be analyzed
	"""

	img = cv2.imread(img_name, cv2.IMREAD_COLOR)
	process_image(img, 0, 0)

if __name__ == "__main__":
	main()