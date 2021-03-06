import numpy as np
from math import degrees, atan2

"""
All code here was brought over from the FCND exercises.
"""

# check to see if the points (p1 - p3) line up to eliminate unnecessary points (p2)
def collinearity_check(p1, p2, p3, epsilon=1e-6):
    m = np.concatenate((p1, p2, p3), 0)
    det = np.linalg.det(m)
    return abs(det) < epsilon


# Convert an array to a point
def point(p):
    return np.array([p[0], p[1], 1.]).reshape(1, -1)


# prune the path down to be "optimized" set of edges.
def prune_path(path):
    pruned_path = [p for p in path]
    i = 0
    while i < len(pruned_path) - 2:
        p1 = point(pruned_path[i])
        p2 = point(pruned_path[i + 1])
        p3 = point(pruned_path[i + 2])

        # If the 3 points are in a line remove the 2nd point.
        # The 3rd point now becomes and 2nd point and the check 
        # is redone with a new third point on the next iteration.
        if collinearity_check(p1, p2, p3):
            # Something subtle here but we can mutate
            # `pruned_path` freely because the length
            # of the list is check on every iteration.
            pruned_path.remove(pruned_path[i + 1])
        else:
            i += 1
    return pruned_path


# Find the closest "valid" point on the graph, based on the current location of the drone.
def closest_point(graph, current_point):
    """
    Compute the closest point in the `graph`
    to the `current_point`.
    """
    cp = None
    dist = 100000
    for p in graph.nodes:
        d = np.linalg.norm(np.array(p) - np.array(current_point))
        if d < dist:
            cp = p
            dist = d
    return cp


# set bearing
def adjust_bearing(waypoints):
    for idx in range(len(waypoints)):
        # skip the first waypoint
        if idx > 0:
            previous_waypoint = waypoints[idx -1]
            current_waypoint = waypoints[idx]
            current_waypoint[3] = np.arctan2((current_waypoint[1] - previous_waypoint[1]), (current_waypoint[0] - previous_waypoint[0]))
    return waypoints
