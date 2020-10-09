import time
from utils import MAX_DIST, distance
from decimal import *

'''
Algorithme Force Brute
Si le nombre de points est suffisamment petit, on préfère utiliser cet algorithme.
'''
def brute_force(points):
    dist_min = MAX_DIST
    points_min = []
    for pos, pt1 in enumerate(points):
        for pt2 in points[(pos+1):]:
            tmp_dist = distance(pt1, pt2)
            if tmp_dist < dist_min:
                dist_min = tmp_dist
                points_min = [pt1, pt2]
    return dist_min, points_min


def execute_brute_force(points):
    getcontext().prec = 50
    start = Decimal(time.time())
    dist_min_bf, points_min_bf = brute_force(points)
    end = Decimal(time.time())
    # print("BF: ", min_brute_force)
    return end-start, dist_min_bf, points_min_bf
