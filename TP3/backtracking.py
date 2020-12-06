from util_init import manDist, isLegalConscrip
from copy import deepcopy
from params import scoreTOL, riskTOL
from itertools import combinations

def backtracking(candidateList, currentConscrip, max_dist, k, depth, currentSum, bestConscrip, bestScore, bestAvailMuniList, visitedList, availMuniList):
	if depth == k:
		availableMuniPerCandidate = getAvailableMuniPerCandidate(candidateList, availMuniList, max_dist)#returns a dict
		return currentConscrip, [currentSum/k, 0], availMuniList, True
	else:
		isValid = False
		maxPossibleScore, minPossibleScore = getPossibleScores(currentSum, k, depth)
		availableMuniPerCandidate = getAvailableMuniPerCandidate(candidateList, availMuniList, max_dist)#returns a dict
		for muni in [x for _,x in sorted(zip(candidateList, availableMuniPerCandidate))]:
			if shouldPruneBranch(maxPossibleScore, minPossibleScore, bestScore):
				return bestConscrip, bestScore, bestAvailMuniList, isValid
			newCandidateList = updateCandidateList(candidateList, muni, max_dist, visitedList)
			newConscrip = currentConscrip.copy()
			newConscrip.append(muni)
			visitedList[muni[0]][muni[1]] = True
			availMuniListCopy = availMuniList.copy()
			availMuniListCopy.remove(muni)
			newSum = currentSum + muni[2]
			resultingConscrip, resultingScore, resultingAvailMuniList, resultIsValid = backtracking(newCandidateList, newConscrip, max_dist, k, depth + 1, newSum, bestConscrip, bestScore, bestAvailMuniList, deepcopy(visitedList), availMuniListCopy)
			if resultIsValid:
				# if muniHasToBeChosen(availableMuniPerCandidate[muni], k):#due to the number of available municipalities for that muni being less than k if it is not chosen for this conscription
					# return resultingConscrip, resultingScore, resultingAvailMuniList, True
				if isNewConscripBetter(bestScore, resultingScore):
					bestConscrip = resultingConscrip
					bestScore = resultingScore
					bestAvailMuniList = resultingAvailMuniList.copy()
					isValid = True
		return bestConscrip, bestScore, bestAvailMuniList, isValid
        
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
		if bestS[0] > 50 and bestS[0] <= 50+scoreTOL:
			return True
		elif minS > 50 and bestS[0] > 50 and bestS[0] <= minS:
			return True
		elif maxS < 50 and (bestS[0] > 50 or bestS[0] <= minS):
			return True
		else:
			return False
	return False

def isNewConscripBetter(oldScore, newScore):#the idea is to aim for a score above 50 and as close as possible, 
	if oldScore:							#but if the score has to be below, go for the smallest possible score so that larger values can be "saved" for future conscriptions
		if oldScore[0] > 50 and newScore[0] <= 50:
			voteScore = -1#scale from -1 to 1 on how tempted we are to choose the new conscrip
		elif oldScore[0] <= 50 and newScore[0] > 50:
			voteScore = 1
		else:#both strictly above 50 or both 50 and below you want to pick the smallest
			voteScore = (oldScore[0] - newScore[0])/50
				
		if voteScore> 0:
			return True
		else:
			return False
	return True
	
def getProximScore(currentConscrip):
	combList = combinations(currentConscrip, 2)
	score = 0
	for comb in combList:
		dist = manDist(comb[0], comb[1])
		score += dist
	return score
	
def updateCandidateList(candidateList, newMuni, max_dist, visitedList):
	newCandidateList = []
	for muni in candidateList:
		dist = manDist(muni, newMuni)
		if(dist <= max_dist and dist>0 and not visitedList[muni[0]][muni[1]]):
			newCandidateList.append(muni)
	return newCandidateList

def getAvailableMuniPerCandidate(candidateList, availMuniList, max_dist):
	dict = {}
	for candidate in candidateList:	
		dict[candidate] = 0
		for muni in availMuniList:
			if isLegalConscrip([candidate], muni, max_dist):
				#dict[candidate].append(muni)
				dict[candidate]+=1
	return dict
			
	
def muniHasToBeChosen(numAvailMuni, k):
	if numAvailMuni < (k-1):
		return True
	return False

def getRiskScore(numAvail, k):
	return max(1 - (numAvail - (k - 1))/((riskTol-1)*(k-1)), -1)
	
def otherChildrenHaveEnoughAvailMuni(availableMuniPerCandidate, resultingConscrip, k):
	count = 0
	stillAvailable = True
	muniInConscrip = False
	for muni in availableMuniPerCandidate:#list of children
		count = 0
		muniInConscrip = False
		for previouslyAvailableMuni in availableMuniPerCandidate[muni]:#list of previously available candidates for the child
			stillAvailable = True
			for conscripMuni in resultingConscrip:#list of now unavailable muni
				if muni == conscripMuni:#muni was added to the conscrip, so no need to check if it is at risk
					muniInConscrip = True
					break
				elif previouslyAvailableMuni == conscripMuni:#find if any of the unavailable munis is the same as the prevAvailable
					stillAvailable == False
					break
			if muniInConscrip:
				break
			if stillAvailable and not muniInConscrip:
				count +=1
		if muniInConscrip:
			pass
		elif count < (k-1)*riskTOL:
			return False
	return True