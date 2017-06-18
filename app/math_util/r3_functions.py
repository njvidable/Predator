import math
from numpy import dot

"""
Calculates the normal vector of a plane that contains the two given vectors.
"""
def get_nv(p1p2v, p1p3v):
    return [float(p1p2v[1] * p1p3v[2] - p1p2v[2] * p1p3v[1]),\
        float(p1p2v[2] * p1p3v[0] - p1p2v[0] * p1p3v[2]),\
            float(p1p2v[0] * p1p3v[1] - p1p2v[1] * p1p3v[0])]
"""
Calculates the 3rd coodinate of a (x,y) point from the plane information.
"""
def get_z(point, pp, nv):
    return (((pp[0] - point[0]) * nv[0] +\
        (pp[1] - point[1]) * nv[1])/ nv[2]) + pp[2]

"""
Calculates the module of a 3D vector.
"""
def module(v):
    return (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** 0.5

"""
Calculates the angle between two given vectors.
"""
def angle_b_vecs(u,v):
    value = dot(u,v)/(module(u) * module(v))
    if math.fabs(value) > 1:
        value = int(value)
    return math.acos(value)

"""
Calculates the matrix that rotates on the given axis "rv" where "a" is the
angle.
"""
def get_rot_mtx(rv, a):#rv = rot_vect, a = angle
    return [[math.cos(a) + rv[0] ** 2 * (1 - math.cos(a)), rv[0] * rv[1] *\
        (1 - math.cos(a)) - (rv[2] * math.sin(a)), rv[0] * rv[2] *\
            (1 - math.cos(a)) + rv[1] * math.sin(a)], [rv[1] * rv[0] *\
                (1 - math.cos(a)) + rv[2] * math.sin(a), math.cos(a) + rv[1]\
                    ** 2 * (1 - math.cos(a)), rv[1] * rv[2] *\
                        (1 - math.cos(a)) - rv[0] * math.sin(a)], [rv[2] *\
                            rv[0] * (1 - math.cos(a)) - rv[1] * math.sin(a),\
                                rv[2] * rv[1] * (1 - math.cos(a)) + rv[0] *\
                                    math.sin(a), math.cos(a) + rv[2] ** 2 *\
                                        (1 - math.cos(a))]]