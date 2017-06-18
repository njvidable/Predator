import cv2

"""
Draws two lines dividing the image in 4 equal pieces.
"""   
def paint_quadrants(img, center, color):
    cv2.line(img, (0, center[1]), (img.shape[1] - 1, center[1]), color, 1)
    cv2.line(img, (center[0], 0), (center[0], img.shape[0] - 1), color, 1)

"""
Draws two lines, diagonal lines connecting nonadjacents vertices.
"""    
def paint_cross(img, color):
    cv2.line(img, (0,0), (img.shape[1], img.shape[0]), color, 1)
    cv2.line(img, (0,img.shape[0]), (img.shape[1], 0), color, 1)

"""
Draws circumferences and their centers.
"""   
def draw_circumferences(img, circles, color):
    for x in circles:
        cv2.circle(img, (x[0][0], x[0][1]), x[1], color, 1)
        img[x[0][1]][x[0][0]] = color

"""
Given a list of points, paints dat pixel with a given color.
"""
def mark_points(img, points, color):
    for x in points: img[x[1]][x[0]] = color

"""
Draws a cricles.
"""
def paint_circle(img, circle, color):
    cv2.circle(img, (circle[0][0], circle[0][1]), circle[1], color, -1)

"""
Draws cricles stored in a list.
"""
def paint_circles(img, circles, color):
    for x in circles: paint_circle(img, x, color)

"""
Draws to show graphically the outcome of the range finder. 
"""
def triangle_info(img, center, fixed_points, px_radius_distances,\
    distance, vangle, hangle):
    from math import degrees
    from sys import path
    from ..math_util.distance_functions import get_poligon_edges
    
    edges = get_poligon_edges(fixed_points, 3)
    cv2.line(img, fixed_points[0], center, (0, 255, 0), 2)
    cv2.putText(img, str(int(px_radius_distances[0])),\
        (fixed_points[0][0] - 40, fixed_points[0][1] + 30),\
            cv2.FONT_HERSHEY_COMPLEX, .75, (0, 255, 0), 1)
    cv2.line(img, fixed_points[1], center, (0, 255, 0), 2)
    cv2.putText(img, str(int(px_radius_distances[1])),\
        (fixed_points[1][0] - 13, fixed_points[1][1] - 20),\
            cv2.FONT_HERSHEY_COMPLEX, .75, (0, 255, 0), 1)
    cv2.line(img, fixed_points[2], center, (0, 255, 0), 2)
    cv2.putText(img, str(int(px_radius_distances[2])),\
        (fixed_points[2][0] + 15, fixed_points[2][1] + 30),\
            cv2.FONT_HERSHEY_COMPLEX, .75, (0, 255, 0), 1)
    cv2.line(img, fixed_points[0], fixed_points[1], (0, 255, 255), 2)
    cv2.putText(img, str(int(edges[0])),(fixed_points[0][0] - 30,\
        fixed_points[0][1] - int(edges[0]/2)), cv2.FONT_HERSHEY_COMPLEX,\
            .75, (0, 255, 255), 1)
    cv2.line(img, fixed_points[1], fixed_points[2], (0, 255, 255), 2)
    cv2.putText(img, str(int(edges[1])),(fixed_points[2][0] - 13,\
        fixed_points[2][1] - int(edges[1]/2)), cv2.FONT_HERSHEY_COMPLEX,\
            .75, (0, 255, 255), 1)
    cv2.line(img, fixed_points[0], fixed_points[2], (0, 255, 255), 2)
    cv2.putText(img, str(int(edges[2])),\
        (center[0] - 15, fixed_points[0][1] + 30),\
            cv2.FONT_HERSHEY_COMPLEX, .75, (0, 255, 255), 1)    
    cv2.putText(img, "{0:.3f}".format(distance) + " mtrs",\
        (center[0] - 38, fixed_points[0][1] + 100),\
            cv2.FONT_HERSHEY_COMPLEX, .75, (255, 0, 0), 1)
    cv2.putText(img, "V Angle: " + "{0:.3f}".format(degrees(vangle))\
        + " degrees", (center[0] - 108, fixed_points[0][1] + 130),\
            cv2.FONT_HERSHEY_COMPLEX, .75, (255, 0, 0), 1)
    cv2.putText(img, "H Angle: " + "{0:.3f}".format(degrees(hangle))\
        + " degrees", (center[0] - 108, fixed_points[0][1] + 160),\
            cv2.FONT_HERSHEY_COMPLEX, .75, (255, 0, 0), 1)

"""
Draws to show graphically the deformation of the cross due to inclination.
"""
def cross_info(img, dots, center):
    from sys import path
    from ..math_util.distance_functions import cal_dist
    #circles order: south, east, west, north
    cv2.line(img, dots[0], center, (0, 255, 255), 2)
    cv2.putText(img, str(int(cal_dist(dots[0], center))),\
        (dots[0][0] - 20, dots[0][1] + 30), cv2.FONT_HERSHEY_COMPLEX,\
            .75, (0, 255, 255), 1)
    cv2.line(img, dots[1], center, (0, 255, 255), 2)
    cv2.putText(img, str(int(cal_dist(dots[1], center))),\
        (dots[1][0] + 10, dots[1][1] + 5), cv2.FONT_HERSHEY_COMPLEX,\
            .75, (0, 255, 255), 1)
    cv2.line(img, dots[2], center, (0, 255, 255), 2)
    cv2.putText(img, str(int(cal_dist(dots[2], center))),\
        (dots[2][0] - 50, dots[2][1] + 5), cv2.FONT_HERSHEY_COMPLEX,\
            .75, (0, 255, 255), 1)
    cv2.line(img, dots[3], center, (0, 255, 255), 2)
    cv2.putText(img, str(int(cal_dist(dots[3], center))),\
        (dots[3][0] - 20, dots[3][1] - 10), cv2.FONT_HERSHEY_COMPLEX,\
            .75, (0, 255, 255), 1)
    
