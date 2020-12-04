from util_init import *
from backtracking import backtracking, getCurrentSum
import time
from params import RANDMUNIRATIO
import sys
import random

FILEPATH = sys.argv[1]
x, y, data = createMuniField(FILEPATH)

start = time.time()

m = random.randint(round(x*y/20), round(x*y/2))
k = 20#round(x*y/m)
randMuniNum = round(RANDMUNIRATIO*k)#within a conscript


initMuni, max_dist = random_init(data, x, y, m)
#print("Full field:", data)
#print(init_candidates)
#print("Proposed chosen municipality: ", initMuni)
#print("Sub-array input to random_expand: ", subC)
failed = True
while(failed):
	newConscrip, failed, visitedList = random_expand(data, initMuni, max_dist, x, y, randMuniNum, 100)
#print("Initial Conscription", newConscrip)
isValid = False
while(not isValid):
	backTrackCandidateList = initCandidateList(data, newConscrip, max_dist, x, y)
	#print("Valid candidates", backTrackCandidateList)
	finalConscrip, finalScore, isValid = backtracking(backTrackCandidateList, newConscrip, max_dist, k, randMuniNum+1, getCurrentSum(newConscrip), None, None, visitedList, False)
	
print("Final Conscription ", finalConscrip)
print("Final Score ", finalScore)
		
		

	
end = time.time()
print("Time ", end - start)
	