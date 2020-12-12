import sys
import os
import math
import random
from copy import deepcopy

def createMuniField(path):	# creates a 2d-list of municipalities [y,x] 
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
	
	for i in range(y):		# Loop over all n munis
		for j in range(x):	# theta(n * inner_loop)
			if(conscripsFilled == a):	# Switch floorVal for ceilVal if a conscrips have been filled [theta(1)]
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

def getInitConscriptions(x, y, data, m):
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
	conscripList = []
	for i in range(m): # empty list of lists
		conscripList.append([])
	
	conscripsFilled = 0
	return dps_greedy(0, 0, x, y, data, conscripList, conscripsFilled, a, ceilVal, floorVal, m, distLim, 0, 0, 1)

def dps_greedy(j, i, x, y, data, conscripList, conscripsFilled, a, ceilVal, floorVal, m, distLim, oldestUnfinishedConscrip, cycleIndex, direction):#where i goes from 0 to y-1, j from 0 to x-1
	#if base case where we have gone through all rows without failing
	print("called, "+str(i)+" "+str(j))
	if i>=y:
		return True, data, conscripList
	#try to add muni to a conscription
	#elif conscripList[oldestUnfinishedConscrip] and i > conscripList[oldestUnfinishedConscrip][0][1]+distLim:#prune
	#	#print(oldestUnfinishedConscrip, conscripList[oldestUnfinishedConscrip][0][1]+distLim)
	#	return False, data, oldestUnfinishedConscrip
	
	muni = data[i][j]#data stores all the municipalities, conscripList stores the current conscriptions
	if(conscripsFilled >= a):	# Switch floorVal for ceilVal if a conscrips have been filled [theta(1)]
		currentMuniLimit = ceilVal
	else:
		currentMuniLimit = floorVal
	for k in range(conscripsFilled, m):
		isLegal = False
		if(len(conscripList[k]) == 0):
			isLegal = True
		else:
			isLegal = isLegalConscrip(conscripList[k], j, i, distLim)
			
		if(isLegal and (len(conscripList[k]) < currentMuniLimit)):#a valid conscription to add muni is found
			data[i][j][3] = k
			conscripList[k].append(data[i][j])
			if(len(conscripList[k]) >= currentMuniLimit):
				conscripsFilledNew = conscripsFilled + 1
				if k == oldestUnfinishedConscrip:
					oldestUnfinishedConscrip = updateOldestUnfinishedConscrip(conscripList, a, ceilVal, floorVal)
			else:
				conscripsFilledNew = conscripsFilled
			
			jNew, iNew, directionNew = getNewIndices(j, i, x, y, cycleIndex, direction)
			#recursive backtracking to get resulting list of conscriptions as well as a isValid bool
			isValid, returnedData, _ = dps_greedy(jNew, iNew, x, y, data, conscripList, conscripsFilledNew, a, ceilVal, floorVal, m, distLim, oldestUnfinishedConscrip, (cycleIndex+1)%4, directionNew)			
			print("return, "+str(i)+" "+str(j))
			#printDists(x, y, returnedData)
			#dps found an answer
			if isValid:
				return True, returnedData, conscripList
			#else dps failed for this muni conscrip pair, try again with a different conscription for this muni
			else:
				data[i][j][3] = None
				conscripList[k].pop()
				#print(oldestUnfinishedConscrip)
				#print(conscripsFilledNew)
				#printDists(x, y, returnedData)
				#print(oldestUnfinishedConscrip, k)
				if not oldestUnfinishedConscrip == k:#break from loop until we are back trying to fill the oldest unfinished conscription #######idea try: save backtrack index instead of conscript number
					return False, data, conscripList
	return False, data, conscriptList #muni cannot be added to any conscription

def updateOldestUnfinishedConscrip(conscripList, a, ceilVal, floorVal):
	k = 0
	currentMuniLimit = None
	for conscrip in conscripList:
		if k < a:
			currentMuniLimit = floorVal
		else:
			currentMuniLimit = ceilVal
		if len(conscrip) < currentMuniLimit:
			return k
		k+=1
	return -1

def getNewIndices(j, i, x, y, currentCycleIndex, direction):#this algo assumes the width is divisable by 2
	if currentCycleIndex == 0:#move from top left to top right (for the direction from left to right case)
		jNew = j + direction
		iNew = i
	elif currentCycleIndex == 1:#move from top right to bottom left
		jNew = j - direction
		iNew = i + 1
	elif currentCycleIndex == 2:#move from bottom left to bottom right
		jNew = j + direction#move along x axis
		iNew = i
	elif currentCycleIndex == 3:#move from bottom right to top left block of next cycle
		jNew = j + direction#move along x axis
		iNew = i - 1
		if jNew >= x or jNew < 0:#change line and direction
			jNew = j
			iNew = i + 1
			direction *= -1
	else:
		print("error")
	return jNew, iNew, direction

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