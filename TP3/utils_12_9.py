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
	return greedyInitialization(0, 0, x, y, data, conscripList, conscripsFilled, a, ceilVal, floorVal, m, distLim, 0, 0, 1)


def greedyInitialization(j, i, x, y, data, conscripList, conscripsFilled, a, ceilVal, floorVal, m, distLim, oldestUnfinishedConscrip, cycleIndex, direction):
	
	while True:
		#print("called, "+str(i)+" "+str(j))
		if i>=y:
			return True, data, conscripList
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
					conscripsFilled = conscripsFilled + 1
				j, i, direction = getNewIndices(j, i, x, y, cycleIndex, direction)
				cycleIndex = (cycleIndex+1)%4
				break#muni is assigned to a conscrip, move on to next
	return False, data, conscriptList #muni cannot be added to any conscription
	

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