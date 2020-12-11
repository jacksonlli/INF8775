from utils_12_9 import *
from backtracking import backtracking, getCurrentSum
import time
from params import RANDMUNIRATIO
import sys
import random

sys.setrecursionlimit(15000)

FILEPATH = sys.argv[1]
M = sys.argv[2]
m = int(M)

x, y, data = createMuniField(FILEPATH)

start = time.time()
isValid, greedyOut = getInitConscriptions(x, y, data, m)
end = time.time()

print(isValid)
print(greedyOut)
printDists(x, y, greedyOut)
print("Time ", end - start)