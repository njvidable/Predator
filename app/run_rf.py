import cv2
import brightest_dots_finder
import trinity_hunter_rev
import matplotlib.pyplot as plt
from painting.paint_functions import paint_cross, paint_quadrants,\
    mark_points, triangle_info
from triangle_analyzer import analyze
from parasyte import fix_points
from math_util.r3_functions import get_z, angle_b_vecs
from math_util.distance_functions import  cal_points_dist
from mpl_toolkits.mplot3d import Axes3D
from multiprocessing import Process

"""
Does the whole range finder job creating instances of "Dots finder"
and "Trinity hunter" in order to filter the brightest dots then recognize
those that belongs to the laser triangle, checking for errors
("Can't find any dot", "Triangle not found").
If no error returns a list of parameters, the outcome of the range finder:
   - plane detected data (normal vector, inclination, distance)
   - convertion factor
   - the process that show the graph of the plane in order to be
     controlled by the ui process
Always an image is returned:
    Error: might be helpfull to get know what the reason is.
    No error: Graphically shows the outcome.
"""
def run(images_path, images_names, area_ratio, threshold_value,\
        mode, hunt_radius):    
    finder = brightest_dots_finder.Brightest_dots_finder(9, threshold_value,\
        255, mode, area_ratio)
    error, msg, thresh, dots = finder.find(images_path, images_names)
    if error:
        return 1, msg, cv2.imread("./resources/error_img.png")
    center = (thresh.shape[1]/2, thresh.shape[0]/2)
    hunter = trinity_hunter_rev.Trinity_hunter_rev(hunt_radius)
    filtered_points = hunter.hunt(center, [x[0] for x in dots]) 
    c_thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    paint_cross(c_thresh, (0, 0, 255))
    paint_quadrants(c_thresh, center, (0, 0, 255))
    if filtered_points is None:
        return 1, "Triangle not found!", c_thresh
    fixed_points = fix_points(thresh, filtered_points, mode)    
    mark_points(c_thresh, filtered_points, (0, 255, 0))
    mark_points(c_thresh, fixed_points, (0, 0, 255))
    px_radius_distances = cal_points_dist(fixed_points, center)
    pp, nv, nvxz, factor = analyze(center, fixed_points, px_radius_distances)
    p = Process(target=plot_graph, args=(pp, nv))
    p.start()
    distance = get_z((0, 0), pp, nv)
    vangle = angle_b_vecs(nv, nvxz)
    hangle = angle_b_vecs(nvxz, [0, 0, nvxz[2]])
    triangle_info(c_thresh, center, fixed_points, px_radius_distances,\
        distance, vangle, hangle)
    return 0, (nv, factor, vangle, hangle, p, distance), c_thresh

"""
Generates and shows the plane detected.
"""
def plot_graph(*args):
    import warnings
    warnings.filterwarnings("ignore")
    X = []
    Y = []
    Z = []
    for y in xrange(-150, 151, 5):
        for x in xrange(-150, 151, 5):
            X.append(x)
            Y.append(-y)
            Z.append(get_z((x, -y), args[0], args[1]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(X, Z, Y, rstride=10, cstride=10)
    plt.show()
