import sys
import os
import math
import random

def createMuniField(path):	# creates a 2d-list of municipalities [y,x] 
				# that is y rows by x columns
	with open(path,"r") as infile:
		xy = infile.readline().split()
		x = int(xy[0])
		y = int(xy[1])
		field = [[0] * x for i in range(y)]
		availableMuni = []
		for j in range(y):
			row = infile.readline().split()
			for k in range(x):
				field[j][k] = int(row[k])
				# if (k==0 and y==0) or (k==x-1 and j==y-1) or (k==0 and j==y-1) or (k==x-1 and j==0):
					#prioritize putting the corners to the front for init municipalities
					# availableMuni.insert(0, (k, j, field[j][k]))
				# else:
				availableMuni.append((k, j, field[j][k]))
	return x, y, availableMuni

def manDist(xy1, xy2):
	return (abs(xy1[0] - xy2[0]) + abs(xy1[1]-xy2[1]))

def isLegalConscrip(conscrip, newMuni, max_dist):#O(n)
	for muni in conscrip:
		dist = manDist(muni, newMuni)
		if(dist > max_dist or dist == 0):
			return False
	return True

def initCandidateList(availMuniList, conscrip, max_dist, x, y):
	candidateList = []
	for muni in availMuniList:
		if isLegalConscrip(conscrip, muni, max_dist):
			candidateList.append(muni)
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

def random_init(availMuni, x, y, m):
	# buffer candidates input and initialize n and max_dist
	choose = random.randint(0, len(availMuni) - 1)
	n = x*y
	max_dist = math.ceil(n/(2*m))
	#print("Max Dist ", max_dist)
	chosenMuni = availMuni.pop(choose)
	return chosenMuni
		
	
def random_expand(availMuni, initMuni, max_dist, x, y, k, iter_lim):
	# add k more random guesses, evaluate if they are legal to form conscription
	# if there do not exist k candidates or iter_lim is reached, return failure
	initConscrip = []
	initConscrip.append(initMuni)
	x0, y0, _ = initMuni
	failed = True
	#print("Begin Expansion Loop...")
	
	for i in range(iter_lim):
		availMuniCopy = availMuni.copy()
		currentConscrip = initConscrip.copy()
		visitedList = [[False for y in range(y)] for i in range(x)]
		if k == 0:
			visitedList[x0][y0] = True
			return initConscrip, False, visitedList, availMuniCopy
		for j in range(k):
			for l in range(round(iter_lim/2)):#attempt to add a muni to the conscrip with limited attempts
				# choose one candidate at random
				choose = random.randint(0, len(availMuniCopy) - 1)
				chosenMuni = availMuniCopy[choose]
				# check if the proposed conscription is legal
				if(isLegalConscrip(currentConscrip, chosenMuni, max_dist)):
					failed = False
					currentConscrip.append(chosenMuni)
					visitedList[chosenMuni[0]][chosenMuni[1]] = True
					availMuniCopy.pop(choose)
					break
				else:
					failed = True
			if failed:#if did not manage to add muni to conscrip, start over from 0
				break
		if not failed: #if successfully added all k muni, return the conscrip
			visitedList[x0][y0] = True
			#print("Expansion Success!")
			return currentConscrip, failed, visitedList, availMuniCopy
	return initConscrip, failed, [], []

def updateAvailableMunicipality(conscrip, availMuniList):
	if conscrip:
		return [x for x in availMuniList if x not in conscrip]
	else:
		return availMuniList

#print(makeCandidates(field, x, y))
#print(field)