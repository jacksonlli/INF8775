from util_init import *
from backtracking import backtracking, getCurrentSum
import time

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
	#print("Valid candidates", candidateList)
	start = time.time()
	finalConscrip, finalScore, isValid = backtracking(candidateList, newConscrip, max_dist, k, randChosenNum+1, getCurrentSum(newConscrip), None, None, visitedList, False)
	end = time.time()
	print("Final Conscription ", finalConscrip)
	print("Final Score ", finalScore)
	
	
	#test for validity of conscript
	# valid = True
	# for i in range(len(finalConscrip)):
		# for j in range(len(finalConscrip)):
			# xi, yi, _ = finalConscrip[i]
			# xj, yj, _ = finalConscrip[j]
			# dist = (abs(xi - xj) + abs(yi - yj))
			# if(dist > max_dist):
				# print("Invalid Value Found ")
				# print(finalConscrip[i], finalConscrip[j])
				# valid = False
	#print("Valid? ", valid)
	
	print("Time ", end - start)
	