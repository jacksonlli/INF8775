from DpR import execute_DpR
from random import randint
from utils import getPointsfromFile
import os

def getNminbyTrialAndError(filepath):
    
    POINTS = getPointsfromFile(filepath)
    sorted_points_x = sorted(POINTS, key=lambda x: x[0])
    sorted_points_y = sorted(POINTS, key=lambda x: x[1])
    
    n_Min = float("inf")
    n_Test = randint(100, 200)
    time_current = float("inf")
    time_previous = float("inf")
    
    while time_current <= time_previous and n_Min > 1:
        n_Min = n_Test
        n_Test = max(int(n_Min / 2), 1)
        time_previous = time_current
        time_current = execute_DpR(sorted_points_x, sorted_points_y, n_Test)[0]
        
    return n_Min
    
    
def getAverageNminForSampleSize(test_directory, n):
    i = 0      
    sumNmin = 0
    path = os.path.join(test_directory,str(n))
    for file in os.listdir(path):
        sumNmin += getNminbyTrialAndError(os.path.join(path, file))
        i += 1
    return int(sumNmin/i)
    
def getOverallAverageNmin(test_directory):
    path = "testsets"
    i = 0
    sumNmin = 0
    for n in os.listdir(path):
        nMin = getAverageNminForSampleSize(test_directory, n)
        print("seuil de recursivité: " + str(nMin) + ", sample size: " + str(n))
        sumNmin += nMin
        i+=1
    return int(sumNmin/i)
    
print(getOverallAverageNmin("testsets"))