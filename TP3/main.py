from utils import *
import time
import sys

FILEPATH = sys.argv[1]
M = sys.argv[2]
m = int(M)
MARKER1 = ""
if (len(sys.argv) >= 4):
    MARKER1 = sys.argv[3]
	
x, y, data = createMuniField(FILEPATH)

#start = time.time()
isValid, greedyOut, conscripList = getInitConscriptions(x, y, data, m)
#end = time.time()
if MARKER1 == 'p':
	printDists(x, y, greedyOut)
else:
	print(score(greedyOut))
#print("Time ", end - start)