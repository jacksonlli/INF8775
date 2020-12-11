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
    print('')

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
                return greedyOut, conscrip
    return greedyOut, conscrip # greedyOut is full

def isLegalConscrip(conscrip, x, y, max_dist):#O(n)
    for muni in conscrip:
        dist = manDist(muni, x, y)
        if(dist > max_dist or dist == 0):
            return False
    return True

def subArrayBounds(x0, y0, distLim, x, y):
    max_dist = math.ceil(distLim / 2)
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

def scoreConscrip(conscripA):
    avg = 0
    for i in range(len(conscripA)):
        avg += conscripA[i][2]
    avg /= len(conscripA)
    wins = (avg > 50)
    return avg, wins
    
def proposedSwap(conscripA, conscripB, currentMuni, proposedMuni):
    pop_indexA, pop_indexB = -1, -1
    
    for i in range(len(conscripA)):
        if (conscripA[i] == currentMuni):
            pop_indexA = i
    conscripA.pop(pop_indexA)
    conscripA.append(proposedMuni)
    for j in range(len(conscripB)):
        if (conscripB[j] == proposedMuni):
            pop_indexB = j
    conscripB.pop(pop_indexB)
    conscripB.append(currentMuni)
    
    return conscripA, conscripB
    


def organizeSwap(x, y, m, conscrip, data):

    # target municipality chosen at random from data
    n = (x*y)
    distLim = math.ceil(n/(2*m))
    chooseX = random.randint(0, (x - 1))
    chooseY = random.randint(0, (y - 1))
    currentMuni = data[chooseY][chooseX]
    currentConscrip = currentMuni[3]
    # establish bounds for a neighborhood centered on the randomly chosen muni
    xMax, xMin, yMax, yMin = subArrayBounds(chooseX, chooseY, distLim, x, y)
    # iterate over all candidates within neighborhood
    p = 0.5         # potential to swap sub-optimally when no clear solution is found
    potentials = [] # storage for potential solutions
    potentialConscrips = []
    for i in range(yMin, yMax):
        for j in range(xMin, xMax):
            thisConscrip = conscrip.copy()
            # skip if the proposed swap is of same conscrip, or if proposing the currentMuni, or if the proposed conscription is illegal
            # assess if swap is legal (swapping data[i][j] w/ currentMuni results in two legal conscrips)
            proposedConscrip = data[i][j][3]
            if((data[i][j][3] != currentMuni[3]) and ((i != currentMuni[1]) and (j != currentMuni[0]))):
                # A represents currentMuni, B the proposed swap muni
                scoreA, Awins = scoreConscrip(thisConscrip[currentConscrip])
                scoreB, Bwins = scoreConscrip(thisConscrip[proposedConscrip])
                # now try the swap and see first if the resulting conscrips are legal
                currentTempCon, propTempCon = proposedSwap(thisConscrip[currentConscrip], thisConscrip[proposedConscrip], currentMuni, data[i][j])
                if(isLegalConscrip(currentTempCon, j, i, distLim) and isLegalConscrip(propTempCon, currentMuni[0], currentMuni[1], distLim)):
                    # if they are legal, check how the score changes due to swap (else no swap)
                    newA, newAwins = scoreConscrip(currentTempCon)
                    newB, newBwins = scoreConscrip(propTempCon)
                    if (((newAwins == True) and (Awins == False)) or ((newBwins == True) and (Bwins == False)) or ()): # If overall score improves, make the swap
                        print('new win')
                        thisConscrip[currentConscrip] = currentTempCon
                        thisConscrip[proposedConscrip] = propTempCon
                        postSwap = data.copy()
                        postSwap[i][j][3] = currentConscrip
                        postSwap[currentMuni[1]][currentMuni[0]][3] = proposedConscrip
                        return postSwap, thisConscrip
                    elif (newAwins != newBwins): # case WL, no improvement (save for swap if both scores come closer to 50)
                        if((abs(50 - scoreA) > abs(50 - newA)) and (abs(50 - scoreB) > abs(50 - newB))):
                            thisConscrip[currentConscrip] = currentTempCon
                            thisConscrip[proposedConscrip] = propTempCon
                            potSwap = data.copy()
                            potSwap[i][j][3] = currentConscrip
                            potSwap[currentMuni[1]][currentMuni[0]][3] = proposedConscrip
                            potentials.append(potSwap)
                            potentialConscrips.append(thisConscrip)
                    elif ((newAwins == False) and (newBwins == False)): # case LL (save for swap if greater of A and B comes closer to 50)
                        if(newA >= newB):
                            if(abs(50 - scoreA) > abs(50 - newA)):
                                thisConscrip[currentConscrip] = currentTempCon
                                thisConscrip[proposedConscrip] = propTempCon
                                potSwap = data.copy()
                                potSwap[i][j][3] = currentConscrip
                                potSwap[currentMuni[1]][currentMuni[0]][3] = proposedConscrip
                                potentials.append(potSwap)
                                potentialConscrips.append(thisConscrip)
                        else:
                            if(abs(50 - scoreB) > abs(50 - newB)):
                                thisConscrip[currentConscrip] = currentTempCon
                                thisConscrip[proposedConscrip] = propTempCon
                                potSwap = data.copy()
                                potSwap[i][j][3] = currentConscrip
                                potSwap[currentMuni[1]][currentMuni[0]][3] = proposedConscrip
                                potentials.append(potSwap)
                                potentialConscrips.append(thisConscrip)
                                
    if((len(potentials) > 0) and (random.random() < p)): # choose randomly from potential solutions given probability p
        n = random.randint(0, len(potentials)-1)
        postSwap = potentials[n]
        conscripOut = potentialConscrips[n]
    else: # no swap performed if there are no potential solutions and probability achieved
        postSwap = data.copy()
        conscripOut = conscrip.copy()            
    return postSwap, conscripOut



    
#print(makeCandidates(field, x, y))
#print(field)