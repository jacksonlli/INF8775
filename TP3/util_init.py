import sys
import os
import math
import random

def createMuniField(path):	# creates a 2d-list of municipalities [y,x] 
				# that is y rows by x columns
	with open(path,"r") as infile:
		xy = infile.readline().split(" ")
		x = int(xy[0])
		y = int(xy[1])
		field = [[0] * x for i in range(y)]
		formattedData = []
		for i in range(x):
			formattedData.append([])
		for j in range(y):
			row = infile.readline().split("  ")
			for k in range(x):
				field[j][k] = int(row[k])
				formattedData[k].append((k, j, field[j][k]))
	return x, y, formattedData

def manDist(xy1, xy2):
	return (abs(xy1[0] - xy2[0]) + abs(xy1[1]-xy2[1]))

def isLegalConscrip(conscrip, newMuni, max_dist):#O(n)
	for muni in conscrip:
		dist = manDist(muni, newMuni)
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

def updateCandidateList(candidateList, newMuni, max_dist):
	newCandidateList = []
	for muni in candidateList:
		dist = manDist(muni, newMuni)
		if(dist <= max_dist):
			newCandidateList.append(muni)
	return newCandidateList

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
	print("Begin Expansion Loop...")
	for i in range(iter_lim):
		currentConscrip = initConscrip.copy()
		visitedList = [[False for y in range(y)] for i in range(x)]
		for j in range(k):
			# choose one candidate at random
			chooseX = random.randint(xMin, xMax)
			chooseY = random.randint(yMin, yMax)
			#print("Proposed addition", data[chooseX][chooseY])
			# check if the proposed conscription is legal
			if(isLegalConscrip(currentConscrip, data[chooseX][chooseY], max_dist)):
				failed = False
				currentConscrip.append(data[chooseX][chooseY])
				visitedList[chooseX][chooseY] = True
			else:
				failed = True
				break
		if not failed:		
			visitedList[x0][y0] = True
			return currentConscrip, failed, visitedList
	return initConscrip, failed, []



	
#print(makeCandidates(field, x, y))
#print(field)