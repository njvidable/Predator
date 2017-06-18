"""
Returns True if at least one element in the list "despl" is 1
"""
def busy(despl):
    return sum(despl) > 0

"""
Another boolean based on the list elements.
"""
def locked(despl):
    return despl[0] == despl[2] and despl[1] == despl[3]

"""
Calculates the moving pattern of the center based in the surrounding
8 pixels.
"""
def calculate_despl_B(image, center, radius):
    return [image[center[1] - radius][center[0]] == 255, #Norte
            image[center[1]][center[0] + radius] == 255, #Este
            image[center[1] + radius][center[0]] == 255, #Sur
            image[center[1]][center[0] - radius] == 255, #Oeste
            image[center[1] - radius][center[0] + radius] == 255, #Noreste
            image[center[1] + radius][center[0] + radius] == 255, #Sureste
            image[center[1] + radius][center[0] - radius] == 255, #Suroeste
            image[center[1] - radius][center[0] - radius] == 255] #Noroeste]

"""
Calculates the moving pattern of the center based in the surrounding
4 pixels.
"""    
def calculate_despl_Z(image, center):
    return [image[center[1] - 1][center[0]] > image[center[1]][center[0]], #N
            image[center[1]][center[0] + 1] > image[center[1]][center[0]], #E
            image[center[1] + 1][center[0]] > image[center[1]][center[0]], #S
            image[center[1]][center[0] - 1] > image[center[1]][center[0]]] #O

"""
Applys the movement calculated to the center
"""
def apply_despl(center, despl, mode):
    center = (center[0], center[1]  - despl[0]) #Norte
    center = (center[0] + despl[1], center[1]) #Este
    center = (center[0], center[1] + despl[2]) #Sur
    center = (center[0] - despl[3], center[1]) #Oeste
    if mode:
        center = (center[0] + despl[4], center[1] - despl[4]) #Noreste
        center = (center[0] + despl[5], center[1] + despl[5]) #Sureste
        center = (center[0] - despl[6], center[1] + despl[6]) #Suroeste
        center = (center[0] - despl[7], center[1] - despl[7]) #Noroeste
    return center

"""
Calls the method to calculate movement based on the parameter mode.
"""
def mode_select(mode):
    def binary_mode(image, center):
        radius = 0
        despl = [1]
        while busy(despl):
            radius = radius + 1
            despl = calculate_despl_B(image, center, radius)        
            center = apply_despl(center, despl, 1)
        return center

    def zero_mode(image, center):
        despl = [0, 0, 1, 1]
        while not locked(despl):
            despl = calculate_despl_Z(image, center)
            center = apply_despl(center, despl, 0)
        return center
        
    mode_dic = {0: binary_mode, 3: zero_mode}
    return mode_dic[mode]

"""
Calculate and applys correction to a list of points choosing a method based
on shape or a intensity based method
"""
def fix_points(image, points, mode):
    f = mode_select(mode)
    return [f(image, x) for x in points]