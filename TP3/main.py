from util_init import *
from backtracking import *

FILEPATH = sys.argv[1]
x, y, data = createMuniField(FILEPATH)

m = 5
k = round(x*y/m)
randChosenNum = 1


initMuni, max_dist = random_init(data, x, y, m)
#print("Full field:", field)
#print(init_candidates)
#print("Proposed chosen municipality: ", initMuni)
#print("Sub-array input to random_expand: ", subC)
newConscrip, failed, visitedList = random_expand(data, initMuni, max_dist, x, y, randChosenNum, 100)
print("Initial Conscription", newConscrip)
if(failed):
	print("this time it failed")
else:
	candidateList = initCandidateList(data, newConscrip, max_dist, x, y)
	print("Valid candidates", candidateList)
	finalConscrip, finalScore, isValid = backtracking(candidateList, newConscrip, max_dist, k, randChosenNum+1, getCurrentSum(newConscrip), None, None, visitedList, False)
	print("Final Conscription ", finalConscrip)
	print("Final Score ", finalScore)
	print(isValid)