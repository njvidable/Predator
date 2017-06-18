import numpy as np
import cv2
from math_util.circle_functions import circle_area, round_circles_coord
from painting.paint_functions import paint_circles

class Brightest_dots_finder():
    def __init__(self, blur_kernel_size, thresh_min, thresh_max,\
        thresh_style, match_coef):
            self.blur_kernel_size = blur_kernel_size
            self.thresh_min = thresh_min
            self.thresh_max = thresh_max
            self.thresh_style = thresh_style
            self.match_coef = match_coef
        
    def find(self, images_path, images_names):
        image = cv2.imread(images_path + "/" + images_names[0], 0)
        shape = image.shape
        del(image)
        thresh = np.zeros((shape[0], shape[1]), np.uint8)
        for x in images_names:
            image = cv2.imread(images_path + "/" + x, 0)
            if not shape == image.shape:
                return 1, "Diferent resolutions @ images folder", None, None  
            thresh = cv2.bitwise_or(thresh, cv2.threshold\
                (cv2.medianBlur(image, self.blur_kernel_size),\
                     self.thresh_min, self.thresh_max, self.thresh_style)[1])
        thresh_copy = np.copy(thresh)
        contours, hierarchy = cv2.findContours(thresh,\
            cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        try:
            chc = zip(contours, hierarchy[0],\
                [cv2.minEnclosingCircle(x) for x in contours])
            _, _, filtered_circles = zip(*filter\
                (lambda x: cv2.contourArea(x[0])/circle_area(x[2]) >\
                    self.match_coef and x[1][2] == -1 and x[1][3] == -1, chc))
        except:
            return 1, "Can't find any dot", None, None
        filtered_circles = round_circles_coord(filtered_circles)
        mask = np.zeros((thresh.shape[0],thresh.shape[1]), np.uint8)
        paint_circles(mask, filtered_circles, (255, 255, 255))
        thresh_masked = cv2.bitwise_and(thresh_copy, mask)
        return 0, " ", thresh_masked, filtered_circles
