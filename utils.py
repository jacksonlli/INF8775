import math

GRID_SIZE = 1000000

MAX_DIST =  math.sqrt(GRID_SIZE**2 + GRID_SIZE**2) # diagonale du carré de côté 1000000

'''
Calcule la distance entre deux points
'''
def distance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

#gets point data from text file
def getPointsfromFile(filepath):
    f = open(filepath, "r")
    numLines = int(f.readline())
    points = []
    for i in range(numLines):
        pointTuple = tuple([int(x) for x in f.readline().split()])
        points.append(pointTuple)
    f.close()
    return points
    
