from math import fabs

class Trinity_hunter:
    def __init__(self, sec_range):
        self.sec_range = sec_range
    
    """
    Returns True when the points amount is lower than 3.
    """
    def no_trinity(self, points):
        return len(points) < 3
    
    """
    Finds out if theres a point in the Southeast quadrant that might be part
    of the triangle.
    """
    def init_condition(self, candidate):
        return candidate[0] > self.center[0] and candidate[1] > self.center[1]

    """
    Finds out if theres a point in the Southwest quadrant that might be part
    of the triangle.
    """
    def mirror_condition(self, candidate):
        return fabs(self.se[1] - candidate[1]) <= self.sec_range\
            and candidate[0] < self.center[0] and candidate[1] >\
                self.center[1]
    
    """
    Finds out if theres a point in the upper quadrants on the center line
    that might be part of the triangle.
    """ 
    def top_condition(self, candidate):
        return fabs(candidate[0] - self.center[0]) <= self.sec_range\
            and candidate[0] < self.se[0] and candidate[0] > self.so[0]\
                and candidate[1] < self.center[1] and candidate[1] < self.se[1]
    
    """
    Looks for a point in the list that satisfy the given condition.
    """ 
    def find_match(self, condition, points):
        for x in points:
            if condition(x):
                return x
        return None
    
    """
    Iterates on the list the searching for triangle process till find it or
    triangle is not found because there are no more candidates.
    """
    def hunt(self, center, points):
        self.center = center
        while not self.no_trinity(points):
            self.se = self.find_match(self.init_condition, points)
            if self.se is None: break
            self.so = self.find_match(self.mirror_condition, points)
            if self.so is not None:
                north = self.find_match(self.top_condition, points)
                if north is not None:
                    return [self.so, north, self.se]
            points.remove(self.se)
        return None