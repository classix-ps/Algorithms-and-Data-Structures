# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 05:02:27 2021

@author: psusk
"""

import copy
import random
import numpy as np
import matplotlib.pyplot as plt

from pylab import rcParams
rcParams['figure.figsize'] = 16, 10

def random_coord(dim=2, minimum=-1, maximum=1):
    return [random.uniform(minimum, maximum) for _ in range(dim)]

def random_plane(points):
    plane = []
    for _ in range(points):
        plane.append(random_coord())
    points = list(zip(*plane))
    plt.scatter(points[0], points[1])
    return plane

def distance(p1, p2):
    return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))

def brute(plane):
    min_dist = float('inf')
    min_points = [[0, 0], [0, 0]]
    operations = 0
    
    for i in range(len(plane) - 1):
        for j in range(i + 1, len(plane)):
            operations += 1
            dist = distance(plane[i], plane[j])
            if dist < min_dist:
                min_dist = dist
                min_points[0] = plane[i]
                min_points[1] = plane[j]
    #plt.scatter([min_points[0][0], min_points[1][0]], [min_points[0][1], min_points[1][1]], s = 20, color='C1')
    return min_dist, min_points, operations

# A utility function to find the
# distance beween the closest points of
# strip of given size. All points in
# strip[] are sorted accordint to
# y coordinate. They all have an upper
# bound on minimum distance as d.
# Note that this method seems to be
# a O(n^2) method, but it's a O(n)
# method as the inner loop runs at most 6 times
def conquer(strip, size, d):
    operations = 0
    # Initialize the minimum distance as d
    min_val = d
    min_points = [[0, 0], [0, 0]]

    # Pick all points one by one and
    # try the next points till the difference
    # between y coordinates is smaller than d.
    # This is a proven fact that this loop
    # runs at most 6 times
    for i in range(size):
        j = i + 1
        while j < size and (strip[j][1] - strip[i][1]) < min_val:
            operations += 1
            min_val = distance(strip[i], strip[j])
            min_points[0] = strip[i]
            min_points[1] = strip[j]
            j += 1

    return min_val, min_points, operations

# A recursive function to find the
# smallest distance. The array P contains
# all points sorted according to x coordinate.
# The array Q contains all points sorted
# according to y coordinate.
def divide(P, Q, n, operations):
    # If there are 2 or points,
    # then use brute force
    if n <= 3:
        b = brute(P)
        return b[0], b[1], operations + b[2]
    
    # Find the middle point
    mid = n // 2
    midPoint = P[mid]

    # Consider the vertical line passing
    # through the middle point calculate
    # the smallest distance dl on left
    # of middle point and dr on right side
    dl, pointsl, operations = divide(P[:mid], Q, mid, operations)
    dr, pointsr, operations = divide(P[mid:], Q, n - mid, operations)

    # Find the smaller of two distances
    if dl < dr:
        d = dl
        points = pointsl
    else:
        d = dr
        points = pointsr

    # Build an array strip[] that contains
    # points close (closer than d)
    # to the line passing through the middle point
    strip = []
    for i in range(n):
        operations += 1
        if abs(Q[i][0] - midPoint[0]) < d:
            strip.append(Q[i])

    # Find the closest points in strip.
    # Return the minimum of d and closest
    # distance is strip[]
    stripD, stripPoints, stripOperations = conquer(strip, len(strip), d)
    if d < stripD:
        return d, points, operations + stripOperations
    else:
        return stripD, stripPoints, operations + stripOperations

# The main function that finds
# the smallest distance.
# This method mainly uses divide()
def divide_and_conquer(P, n):
    operations = 0
    P.sort(key = lambda point: point[0])
    Q = copy.deepcopy(P)
    Q.sort(key = lambda point: point[1])

    # Use recursive function divide()
    # to find the smallest distance
    return divide(P, Q, n, operations)
  
plane = random_plane(50)
b = brute(plane)           
print(b[0], b[2])
plt.scatter([b[1][0][0], b[1][1][0]], [b[1][0][1], b[1][1][1]], s = 20, color='C1')
d = divide_and_conquer(plane, len(plane))
print(d[0], d[2])
plt.scatter([b[1][0][0], b[1][1][0]], [b[1][0][1], b[1][1][1]], s = 5, color='C2')