from DpR import execute_DpR
from random import randint
from utils import getPointsfromFile
import os

#code used to trial and test the recursion threshold until we find one that performs better than its neighbors.

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
    i = 0
    sumNmin = 0
    fn = os.path.join("nmin", "n_Min_by_trial_and_error.txt")
    with open(fn, 'w') as f:
        for n in os.listdir(test_directory):
            nMin = getAverageNminForSampleSize(test_directory, n)
            print("seuil de recursivité: " + str(nMin) + ", sample size: " + str(n))
            f.write("seuil de recursivité: " + str(nMin) + ", sample size: " + str(n) + '\n')    
            sumNmin += nMin
            i+=1
        f.write("seuil de recursivité moyenne: " + str(int(sumNmin/i)) + '\n')
    f.close()
    return int(sumNmin/i)
    
print(getOverallAverageNmin("testsets"))