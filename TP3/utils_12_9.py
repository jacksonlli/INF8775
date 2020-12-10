import sys
import os
import math
import random

def createMuniField(path):  # creates a 2d-list of municipalities [y,x] 
                # that is y rows by x columns
    with open(path,"r") as infile:
        xy = infile.readline().split()
        x = int(xy[0])
        y = int(xy[1])
        formattedData = []
        for i in range(y): # formattedData is a list of lists
            formattedData.append([])
        for j in range(y):
            row = infile.readline().split()
            for k in range(x):
                formattedData[j].append([k, j, int(row[k]), None]) # each entry of fD is a list (x, y, vote, district (initially None))
    return x, y, formattedData

def manDist(xy1, x2, y2):
    return (abs(xy1[0] - x2) + abs(xy1[1]-y2))
    
def printDists(x, y, data):
    for j in range(y):
        line = []
        for i in range(x):
            line.append(data[j][i][3])
        print(line)

def greedy(x, y, data, m): # input is a list of lists from cMF above
# greedy will cycle through entries and assign each to legal districts in order of the districts' instantiation

    greedyOut = data.copy()

    n = (x*y)
    distLim = math.ceil(n/(2*m))
    floorVal = math.floor(n/m)
    ceilVal = math.ceil(n/m)
    if (floorVal == ceilVal):
        a = m
        b = 0
    else:
        a = ceilVal*m - n
        b = m - a
        
    conscrip = []
    for i in range(m): # empty list of lists
        conscrip.append([])
    
    currentMuniLimit = floorVal # start by filling each conscription with k = floorVal, after 'a' conscrips are filled, switch to k = ceilVal 
    conscripsFilled = 0
    
    for i in range(y):      # Loop over all n munis
        for j in range(x):  # theta(n * inner_loop)
            if(conscripsFilled == a):   # Switch floorVal for ceilVal if a conscrips have been filled [theta(1)]
                currentMuniLimit = ceilVal
            for k in range(conscripsFilled,m):
                #print(conscrip[k])
                #printDists(x, y, greedyOut)
                isLegal = False
                if(len(conscrip[k]) == 0):
                    isLegal = True
                else:
                    isLegal = isLegalConscrip(conscrip[k], j, i, distLim)
                if(isLegal and (len(conscrip[k]) < currentMuniLimit)):
                    greedyOut[i][j][3] = k
                    conscrip[k].append(greedyOut[i][j])
                    if(len(conscrip[k]) >= currentMuniLimit):
                        conscripsFilled = conscripsFilled + 1
                    break
            if(greedyOut[i][j][3] == None):
                return greedyOut
    return greedyOut # greedyOut is full

def isLegalConscrip(conscrip, x, y, max_dist):#O(n)
    for muni in conscrip:
        dist = manDist(muni, x, y)
        if(dist > max_dist or dist == 0):
            return False
    return True

def initCandidateList(data, conscrip, max_dist, x, y):
    x0, y0, _ = conscrip[0]
    xMax, xMin, yMax, yMin = subArrayBounds(x0, y0, max_dist, x, y)
    candidateList = []
    for i in range(xMin, xMax + 1):
        for j in range(yMin, yMax + 1):
            if isLegalConscrip(conscrip, data[i][j], max_dist):
                candidateList.append(data[i][j])
    return candidateList


def subArrayBounds(x0, y0, max_dist, x, y):
    xMax = x0 + max_dist
    xMin = x0 - max_dist
    yMax = y0 + max_dist
    yMin = y0 - max_dist
    if (xMax > (x-1)):
        xMax = x-1
    if (xMin < 0):
        xMin = 0
    if (yMax > (y-1)):
        yMax = y-1
    if (yMin < 0):
        yMin = 0
    return xMax, xMin, yMax, yMin

def random_init(data, x, y, m):
    # buffer candidates input and initialize n and max_dist
    n = x*y
    max_dist = math.ceil(n/(2*m))
    print("Max Dist ", max_dist)
    # choose a random candidate
    chooseX = random.randint(0, (x - 1))
    chooseY = random.randint(0, (y - 1))
    # remove the choice and save it for return (this is the first muni in the proposed conscrip)
    initMuni = data[chooseX][chooseY]   
    return initMuni, max_dist
    
def random_expand(data, initMuni, max_dist, x, y, k, iter_lim):
    # add k more random guesses, evaluate if they are legal to form conscription
    # if there do not exist k candidates or iter_lim is reached, return failure
    initConscrip = []
    initConscrip.append(initMuni)
    x0, y0, _ = initMuni
    xMax, xMin, yMax, yMin = subArrayBounds(x0, y0, max_dist, x, y)
    failed = True
    print("Begin Expansion Loop...")
    for i in range(iter_lim):
        currentConscrip = initConscrip.copy()
        visitedList = [[False for y in range(y)] for i in range(x)]
        for j in range(k):
            for l in range(round(iter_lim/2)):#attempt to add a muni to the conscrip with limited attempts
                # choose one candidate at random
                chooseX = random.randint(xMin, xMax)
                chooseY = random.randint(yMin, yMax)
                #print("Proposed addition", data[chooseX][chooseY])
                # check if the proposed conscription is legal
                if(isLegalConscrip(currentConscrip, data[chooseX][chooseY], max_dist)):
                    failed = False
                    currentConscrip.append(data[chooseX][chooseY])
                    visitedList[chooseX][chooseY] = True
                    break
                else:
                    failed = True
            if failed:#if did not manage to add muni to conscrip, start over from 0
                break
        if not failed: #if successfully added all k muni, return the conscrip
            visitedList[x0][y0] = True
            print("Expansion Success!")
            return currentConscrip, failed, visitedList
    return initConscrip, failed, []



    
#print(makeCandidates(field, x, y))
#print(field)