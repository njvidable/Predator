import cv2
import numpy as np
import glob
import sys
sys.path.insert(1, "../")
from json_trade.json_functions import data_to_json

# Writes down a list of objects (the calculated camera parameters) using json

def write_down(objects):
    with open("../camera_data/camera_parameters.txt", "w") as fd:
        for obj in objects:
            fd.write(data_to_json(obj)+ "\n")

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9, 3), np.float32)
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('./input_images/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH +
        cv2.cv.CV_CALIB_CB_NORMALIZE_IMAGE)
    
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        cv2.cornerSubPix(gray,corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (9,6), corners, ret)
        cv2.imwrite('./output_images/' + fname[15:], img)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print "Optimized reprojection error: " + str(ret)

tot_error = 0
for i in xrange(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    tot_error += error

print "Mean error: ", tot_error/len(objpoints)

"""
calibrateCamera returns the root mean square (RMS) re-projection error, usually it should be
between 0.1 and 1.0 pixels in a good calibration. The calculation is done by projecting the
3D chessboard points (objectPoints) into the image plane using the final set of calibration
parameters (cameraMatrix, distCoeffs, rvecs and tvecs) and comparing the known position of
the corners (imagePoints).

An RMS error of 1.0 means that, on average, each of these projected points is 1.0 px away 
from its actual position. The error is not bounded in [0, 1], it can be considered as a
distance.
"""

h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

write_down([img.shape, mtx, dist, roi, newcameramtx])

for fname in images:    
    # undistort
    dst = cv2.undistort(cv2.imread(fname), mtx, dist, None, newcameramtx)
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst2 = cv2.remap(cv2.imread(fname), mapx, mapy, cv2.INTER_LINEAR)
    
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    dst2 = dst2[y:y+h, x:x+w]
    cv2.imwrite('./undistortion_undistort_result/'+ fname[15:], dst)
    cv2.imwrite('./undistortion_remapping_result/'+ fname[15:], dst2)
    
