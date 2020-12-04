from util_init import manDist
from copy import deepcopy

def backtracking(candidateList, currentConscrip, max_dist, k, depth, currentSum, bestConscrip, bestScore, visitedList, isValid):
	if depth == k:
		return currentConscrip, currentSum/k, True
	else:
		maxPossibleScore, minPossibleScore = getPossibleScores(currentSum, k, depth)
		for muni in candidateList:
			if shouldPruneBranch(maxPossibleScore, minPossibleScore, bestScore):
				return bestConscrip, bestScore, isValid
			newCandidateList = updateCandidateList(candidateList, muni, max_dist, visitedList)
			newConscrip = currentConscrip.copy()
			newConscrip.append(muni)
			visitedList[muni[0]][muni[1]] = True
			
			newSum = currentSum + muni[2]
			resultingConscrip, resultingScore, isValid = backtracking(newCandidateList, newConscrip, max_dist, k, depth + 1, newSum, bestConscrip, bestScore, deepcopy(visitedList), isValid)
			if isNewConscripBetter(bestScore, resultingScore):
				bestConscrip = resultingConscrip
				bestScore = resultingScore
		return bestConscrip, bestScore, isValid
        
def getPossibleScores(currentSum, k, currentSize):
	maxPossibleScore = (currentSum + 100*(k - currentSize))/k
	minPossibleScore = currentSum/k
	return maxPossibleScore, minPossibleScore
	
def getCurrentSum(currentConscrip):
	currentSum = 0
	for muni in currentConscrip:
		currentSum += muni[2]
	return currentSum
	
def shouldPruneBranch(maxS, minS, bestS):
	if bestS:
		if bestS > 50 and bestS <= 50.1:
			return True
		elif minS > 50 and bestS > 50 and bestS <= minS:
			return True
		elif maxS < 50 and (bestS > 50 or bestS <= minS):
			return True
		else:
			return False
	return False
	
def isNewConscripBetter(oldScore, newScore):#the idea is to aim for a score above 50 and as close as possible, 
	if oldScore:							#but if the score has to be below, go for the smallest possible score so that larger values can be "saved" for future conscriptions
		if oldScore > 50 and newScore <= 50:
			return False
		elif oldScore <= 50 and newScore > 50:
			return True
		else:#both strictly above 50 or both 50 and below you want to pick the smallest
			return True if newScore < oldScore else False
	return True
	
def updateCandidateList(candidateList, newMuni, max_dist, visitedList):
	newCandidateList = []
	for muni in candidateList:
		dist = manDist(muni, newMuni)
		if(dist <= max_dist and dist>0 and not visitedList[muni[0]][muni[1]]):
			newCandidateList.append(muni)
	return newCandidateList