from util_init import *
from backtracking import backtracking, getCurrentSum
import time
from params import RANDMUNIRATIO
import sys
import random
from copy import deepcopy

sys.setrecursionlimit(10000)  

FILEPATH = sys.argv[1]
x, y, availableMuniOriginal = createMuniField(FILEPATH)


m = int(sys.argv[2])
k = round(x*y/m)
randMuniNum = round(RANDMUNIRATIO*k)#within a conscript

bestScore = -999999999
bestSolution = []
max_dist = math.ceil(x*y/(2*m))

solutionScore = 0
solutionList = []
start = time.time()
availableMunicipalities = []
initMuni = None
newConscrip = []
isExpandFailed = True
visitedList = []
backTrackCandidateList =[]
finalConscrip = []
finalScore = None
isBTValid = False

while(True):
	availableMunicipalities = availableMuniOriginal.copy()
	solutionScore = 0
	solutionList = []
	start = time.time()
	for i in range(m):
		
		initMuni = availableMunicipalities.pop(0)#random_init(availableMunicipalities, x, y, m)
		newConscrip, isExpandFailed, visitedList = random_expand(availableMunicipalities, initMuni, max_dist, x, y, randMuniNum, 100)
		if isExpandFailed:
			break
		backTrackCandidateList = initCandidateList(availableMunicipalities, newConscrip, max_dist, x, y)
		finalConscrip, finalScore, isBTValid = backtracking(backTrackCandidateList, newConscrip, max_dist, k, randMuniNum+1, getCurrentSum(newConscrip), None, None, visitedList, False)
		availableMunicipalities = updateAvailableMunicipality(finalConscrip, availableMunicipalities)
		if not isBTValid:
			break
		if finalScore > 50:
			solutionScore += 1
		solutionList.append(finalConscrip)	
	if isExpandFailed or not isBTValid:
		#print("fail")
		pass
	elif solutionScore > bestScore:
		bestScore = solutionScore
		bestSolution = solutionList
		print(bestSolution)
		end = time.time()
		print("Time ", end - start)
		#printSolution(bestSolution)
		start = time.time()
	else:
		print("iteration done")
		print("Time ", end - start)
		start = time.time()
	end = time.time()
	
	