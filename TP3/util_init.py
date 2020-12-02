import sys
import os
import math
import random

FILEPATH = sys.argv[1]

def createMuniField(path):  # creates a 2d-list of municipalities [y,x] 
				# that is y rows by x columns
	with open(path,"r") as infile:
		xy = infile.readline().split(" ")
		x = int(xy[0])
		y = int(xy[1])
		field = [[0] * x for i in range(y)]
		init_candidates = []
		for j in range(y):
			row = infile.readline().split("  ")
			for k in range(x):
				field[j][k] = int(row[k])
				init_candidates.append((k, j, field[j][k]))
	return field, x, y, init_candidates

def manDist(xy1, xy2):
	return (abs(xy1[0] - xy2[0]) + abs(xy1[1]-xy2[1]))

def isLegalConscrip(conscrip, max_dist):
	# THIS IS O(n^2) can that be fixed????
	for i in range(len(conscrip)):
		for j in range(len(conscrip)):
			xi, yi, _ = conscrip[i]
			xj, yj, _ = conscrip[j]
			dist = (abs(xi - xj) + abs(yi - yj))
			if(dist > max_dist):
				return False
	return True

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

def random_init(C, x, y, m):
	# buffer candidates input and initialize n and max_dist
	initC = C
	n = x*y
	max_dist = math.ceil(n/(2*m))
	# choose a random candidate
	choose = random.randint(0, (len(initC) - 1))
	# remove the choice and save it for return (this is the first muni in the proposed conscrip)
	initMuni = initC.pop(choose)	
	# limit candidates to the subarray (max_dist about the random choice)
	x0, y0, _ = initMuni
	xMax, xMin, yMax, yMin = subArrayBounds(x0, y0, max_dist, x, y)

	# loop through all remaining candidates (excluding initMuni) to create more precise list of candidates
	newC = []
	for i in range(len(initC)):
		currentX, currentY, _ = initC[i]
		if ((currentX <= xMax) and (currentX >= xMin) and (currentY <= yMax) and (currentY >= yMin)):
			newC.append(initC[i])
	
	return newC, initMuni, max_dist

def random_expand(C, initMuni, max_dist, k, iter_lim):
	# add k more random guesses, evaluate if they are legal to form conscription
	# if there do not exist k candidates or iter_lim is reached, return failure
	failed = True
	initC = C.copy()
	initConscrip = []
	initConscrip.append(initMuni)
	if (len(initC) < k):
		newC = initC
		newConscrip = initConscrip
	else:
		print("Begin Expansion Loop...")
		for i in range(iter_lim):
			currentC = initC.copy()
			currentConscrip = initConscrip.copy()
			for j in range(k):
				# choose one candidate at random
				choose = random.randint(0, (len(currentC)-1))
				# remove it from the current candidate list and add it to the current conscription
				currentConscrip.append(currentC.pop(choose))
				print("Current Candidates: ", currentC)
				print("Proposed conscription", currentConscrip)
			# check if the proposed conscription is legal
			if(isLegalConscrip(currentConscrip, max_dist)):
				failed = False
				return currentC, currentConscrip, failed
		newC = initC
		newConscrip = initConscrip	
	return newC, newConscrip, failed

field,x,y,init_candidates = createMuniField(FILEPATH)
subC, initMuni, max_dist = random_init(init_candidates, x, y, 5)
print("Full field:", field)
print("Proposed chosen municipality: ", initMuni)
print("Sub-array input to random_expand: ", subC)
newC, newConscrip, failed = random_expand(subC, initMuni, max_dist, 2, 100)

if(failed):
	print("this time it failed")
else:
	print("Remaining Candidates: ", newC)
	print("Randomly Proposed Conscription: ", newConscrip)

#print(makeCandidates(field, x, y))
#print(field)