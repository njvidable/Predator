"""
Returns True if the point is outside the circle.
"""
def is_outside_circle(point, circle):
    return (point[0] - circle[0][0]) ** 2 +\
        (point[1] - circle[0][1]) ** 2 > circle[1] ** 2

"""
Returns True if the point is inside the circle.
"""
def is_inside_circle(point, circle): #  (y-b)^2 + (x-a)^2 <= radius^2
    return (point[0] - circle[0][0]) ** 2 +\
        (point[1] - circle[0][1]) ** 2 <= circle[1] ** 2

"""
Calculates the area of a given circle.
"""
def circle_area(circle):
    return 3.14 * (circle[1] ** 2)

"""
Make the coodinates of a circle rounded int numbers.
"""
def round_circles_coord(circles):
    return [((int(round(x[0][0])), int(round(x[0][1]))),\
        int(round(x[1]))) for x in circles]

"""
Given a list of circles if the given point is inside one of the circles, 
returns True and the index of the circle otherwise returns False and -1 as
index.
"""
def is_within_circles(point, circles):
    for x in circles:
        if is_inside_circle(point, x):
            return (True, circles.index(x))
    return (False, -1)