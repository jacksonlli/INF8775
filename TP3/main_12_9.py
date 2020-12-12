from utils_12_9 import *
from backtracking import backtracking, getCurrentSum
import time
from params import RANDMUNIRATIO
import sys
import random

FILEPATH = sys.argv[1]
M = sys.argv[2]
m = int(M)

x, y, data = createMuniField(FILEPATH)

start = time.time()
isValid, greedyOut, conscripList = getInitConscriptions(x, y, data, m)
print("done!")
end = time.time()
printDists(x, y, greedyOut)
print("Time ", end - start)