"""
Calculates the distance between two points in 2D.
"""
def cal_dist(a, b):
    return round(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5, 0)

"""
Calculates the distance of a list of points to an specific point.
"""
def cal_points_dist(points, point):
    return [cal_dist(x, point) for x in points]

"""
Calculates the edges of a poligon.
points: list of points that describes the poligon, must be sorted.
edges_number: number of edges.
"""
def get_poligon_edges(points, edges_number):
    return [cal_dist(points[x], points[(x+1) % edges_number])\
        for x in xrange(edges_number)]

"""
Given a list of points, calcules the closest to an specific point.
"""
def get_closest(orig, points):
    acc = cal_dist(orig, points[0])
    closest = points[0]
    for x in points:
        distance = cal_dist(orig, x) 
        if  distance < acc:
            closest = x
            acc = distance
    return closest