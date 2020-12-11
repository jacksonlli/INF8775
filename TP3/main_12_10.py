from utils_12_9 import *
from backtracking import backtracking, getCurrentSum
import time
from params import RANDMUNIRATIO
import sys
import random

def scoreField(conscrip):
    score = 0
    for i in range(len(conscrip)):
        _, thisWins = scoreConscrip(conscrip[i])
        if(thisWins):
            score = score + 1
    return score
    

FILEPATH = sys.argv[1]
M = sys.argv[2]
m = int(M)

x, y, data = createMuniField(FILEPATH)

data, conscrip = greedy(x, y, data, m)
init_conscrip = conscrip.copy()

printDists(x, y, data)

bestData = data.copy()
bestScore = scoreField(conscrip)

while(True):
    data, conscrip = organizeSwap(x, y, m, conscrip, data)

    thisScore = scoreField(conscrip)
    if(thisScore > bestScore):
        bestData.clear()
        bestData = data.copy()
        bestScore = thisScore
        printDists(x, y, bestData)