from math import cos, pi
from measure_functions import *
from math_util.r3_functions import get_nv

"""
Calculates the edges of the triangle based on radius values
then gets the distance [mtrs] of each vertex
"""
def transform_distances(px_radius_distances):
    return [transform(2 * x * cos(pi/6))
        for x in px_radius_distances]

"""
Given a list of three points (x,y) and another with the same size containing
the 3rd coordinate for these. In other words the parameters are three points
in R3. Then calculates two vectors. 
"""
def vecs_4_plane(xy, z):
    return [xy[1][0] - xy[0][0], xy[1][1] - xy[0][1], z[1] - z[0]],\
        [xy[2][0] - xy[0][0], xy[2][1] - xy[0][1], z[2] - z[0]] 

"""
Uses "transform_distances" in order to get the distance of each vertex. The
average of these three distances is the distance to the center of the plane.
The convertion factor is calculated with the distance of the center.
The factor is used to convert the pixel coordinates of the laser dots detected
in the working image into coodrinates in meter unit.
Having coodinates three points in meter unit, calculates the normal vector
to the plane that leads to the inclination.
Returns a point that belongs to the detected plane, normal vector and its
projection on the xz plane, the convertion factor.
"""            
def analyze(center, fixed_centers, px_radius_distances):
    mtr_dists = transform_distances(px_radius_distances)
    center_dist = sum(mtr_dists) / 3
    factor = get_factor(transform(center_dist))
    fixed_centers = [((x[0] - center[0]) * factor,\
        (center[1] - x[1]) * factor) for x in fixed_centers]
    p1p2v, p1p3v = vecs_4_plane(fixed_centers, mtr_dists)
    nv = get_nv(p1p2v, p1p3v)
    return (fixed_centers[0][0], fixed_centers[0][1], mtr_dists[0]),\
        nv, [nv[0], 0, nv[2]], factor
