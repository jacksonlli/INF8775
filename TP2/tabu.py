from utils import createBlocks, printBlocks
import sys
import numpy as np
import time


def mustReplace(c,s):
	fitsAbove = (c[1] < s[1]) and (c[2] < s[2]) #candidate fits above if the 2 surface dimensions are strictly less than the solution block
	fitsBelow = (c[1] > s[1]) and (c[2] > s[2]) #candidate fits below if the 2 surface dimension are strictly greater than the solution block
	# replace if the candidate does not fit above or below the sol'n block, or the sol'n block shares the candidate ID
	replace =  not (fitsAbove or fitsBelow) # or (c[3] == s[3])
	
	return replace, fitsAbove, fitsBelow
	

def tabu_score(c,S):
	# c is a member of Candidates (C) and S is the proposed solution
	# score is the tabu score of this candidate's inclusion in the stack
	# score = -(height of blocks replaced) + (height of c)
	score = c[0] # height is the first entry of each candidate
	# Different paradigm if S is 1D (S only consists of one block)
	if(S.ndim > 1):
		for i in range(S.shape[0]):
			replace, _ , _ = mustReplace(c,S[i])
			if(replace):
				score -= S[i,0]
	else:
		replace, _ , _ = mustReplace(c,S)
		if(replace):
			score -= S[0]
	return score

def scoring(C,S):
# Scoring	# Find tabu High score and associated Tabu blocks
	hi_score = -1000000
	hiC_index = 0
	for i in range(C.shape[0]):
		score = tabu_score(C[i],S)
		if (score > hi_score):
			hi_score = score
			hiC_index = i

	return hi_score, hiC_index

def updateS(c,S):
# Add best Candidate to solution
	tabBlocks = np.array([[]])
	if(S.ndim == 1): # If S is 1D
		replace, fitsAbove, fitsBelow = mustReplace(c,S)
		if(replace):
			newS = c
			tabBlocks = S
		elif(fitsBelow):
			newS = np.vstack((c,S))
		elif(fitsAbove):
			newS = np.vstack((S,c))
	else:
		replaceIndices = [] # indices of parts of the solution to replace
		tabBlocks = np.zeros(6,int) # blocks bound for T
		for i in range(S.shape[0]):
			replace, _ , _ = mustReplace(c,S[i])
			if(replace):
				if (len(replaceIndices) == 0):
					replaceIndices = [i]
				else:
					replaceIndices += [i]
				tab = np.append(S[i],np.random.randint(7,11))
				tabBlocks = np.vstack((tabBlocks,tab))
		#print("replaceIndices: ",replaceIndices)
		# Delete bad blocks from S to form newS
		newS = np.delete(S,replaceIndices,0)
		# handle tabBlocks
		if(tabBlocks.ndim == 1): # if no blocks are replaced
			tabBlocks = np.array([])
		else: # if not, discard the initialization value
			tabBlocks = np.delete(tabBlocks, 0, 0)
			
		# now fit c to newS
		if(newS.ndim == 1): # If newS is 1D
			_ , fitsAbove, fitsBelow = mustReplace(c,newS)
			if(fitsBelow):
				newS = np.vstack((c,S))
			elif(fitsAbove):
				newS = np.vstack((S,c))
		else:
			# if c fits below the base of the tower, stack on it
			_ , _ , fitsBelow = mustReplace(c,newS[0])
			if(fitsBelow):
				newS = np.vstack((c,newS))
			else:
				inserted = False
				for j in range(newS.shape[0]):
					_ , _ , fitsBelow = mustReplace(c,newS[j])
					if(fitsBelow and (not inserted)):
						newS = np.insert(newS, (j), c, 0)
						inserted = True	
		

	#print("newS: ", newS)
	#print("tabBlocks: ",tabBlocks)
	return newS, tabBlocks

def appendTabBlocks(T,tabBlocks):
	if(T.size == 0):
		appendedT = tabBlocks
	elif(tabBlocks.size == 0):
		appendedT = T
	else:
		appendedT = np.vstack((T,tabBlocks))
	return appendedT

def updateT(T,tabBlocks, C):
	# the following function adds the new tabu blocks to T
	currentT = appendTabBlocks(T,tabBlocks)

	# there are three possible cases
	# if the currentT is empty, do nothing
	if(currentT.size == 0): # if there are no tabu blocks to add, pass
		newT = currentT
		newC = C
	# if currentT is 1D vector
	elif(currentT.ndim == 1):
		#decrement the tabu counter	
		currentT[5] -= 1
		#if we hit zero on tabu counter
		# stack the tabu block back onto the candidates 
		if(currentT[5] == 0):
			newCandidate = np.delete(currentT,5)
			newC = np.vstack((C, newCandidate))
			newT = np.array([])
		# if we don't hit zero on tabu counter, pass
		else:
			newT = currentT
			newC = C
	# if currentT is 2D
	elif(currentT.ndim > 1):
		# we instantiate newT with this dummy value so that we can use np.vstack(())
		newT = np.zeros(6,int)
		# we want to stack any spent tabu blocks back under the Candidates
		newC = C	
		for i in range(currentT.shape[0]): 	# iterate over Tabu list
			currentT[i,5] -= 1 		# decrement tabu counter value
			if(currentT[i,5] == 0):		# if counter zero stack the current tabu block under C
				newCandidate = np.delete(currentT[i],5,0)
				newC = np.vstack((newC,newCandidate))
			else:				# else, stack current block in newT
				newT = np.vstack((newT,currentT[i]))
		# Two cases:
		# if newT is empty (apart from dummy value)
		if(newT.ndim == 1):
			newT = np.array([])
		# else, delete dummy variable
		else:
			newT = np.delete(newT,0,0)
	return newT, newC
	
			
	
def tabu_search(blocks):
	# Initial Candidates and Solution sets formed
	C = blocks
	i_0 = np.argmax(C[:,0]) # index of largest h
	prevS = np.zeros(5,int)
	prevS = C[i_0]
	bestS = prevS
	bestH = prevS[0]
	C = np.delete(C, i_0, 0)
	T = np.array([])
	convCount = 0

	while(convCount < 100):

		hi_score, hiC_index = scoring(C,prevS)
		#print("best c: ",C[hiC_index])

		#print("prevS: ",prevS)
		
		newS, tabBlocks = updateS(C[hiC_index],prevS)

		C = np.delete(C,hiC_index,0)
	
		T, C = updateT(T, tabBlocks, C)


# Update bestS	# compare height of resulting tower to height of best Solution
		# if thisH <= bestH, we increment convCount
		newH = np.sum(newS, axis=0)[0]
		if(newH > bestH):
			bestH = newH
			bestS = newS
			convCount = 0
		else:
			convCount += 1
		prevS = newS

	return bestH, bestS[:, 0:3]

def execute_tabu_search(blocks):
	start = time.time()
	height, blockList = tabu_search(blocks)
	#print(blockList)
	#print(height)
	end = time.time()
	return (end - start), height, blockList