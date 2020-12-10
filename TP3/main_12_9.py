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

greedyOut = greedy(x, y, data, m)

print(greedyOut)
printDists(x, y, greedyOut)



	