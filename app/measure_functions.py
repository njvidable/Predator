"""
Transform a pixel measure to meters and the other way around.
"""
def transform(x):
    return 156.25 / x

"""
Calculates the convertion factor based on the edge of the equilateral
triangle calculated from the distance to the plane of projection.
"""
def get_factor(eqtriangle_edge_px_dist):
    return 0.11 / eqtriangle_edge_px_dist