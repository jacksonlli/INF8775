import csv
from utils import threshold_Experimental, threshold_Arbitrary, getPointsfromFile
from DpR import execute_DpR
from brute_force import execute_brute_force
import os

#runs the all three algorithms on all testsets and writes everything into a csv file.

test_directory = "testsets"

with open('data.csv', 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Sample','Sample Size','Brute Force', 'Divide and Conquer', 'D&C with Experimental Recursion Threshold'])
    for n in os.listdir(test_directory):
        if str(n) == "10" or str(n) == "100" or str(n) == "50":
            path = os.path.join(test_directory,str(n))
            for file in os.listdir(path):
                print(file)
                POINTS = getPointsfromFile(os.path.join(path, file))
                sorted_points_x = sorted(POINTS, key=lambda x: x[0])
                sorted_points_y = sorted(POINTS, key=lambda x: x[1])
                
                time_BF = execute_brute_force(sorted_points_x)[0]
                time_DpR = execute_DpR(sorted_points_x, sorted_points_y, threshold_Arbitrary)[0]
                time_seuil = execute_DpR(sorted_points_x, sorted_points_y, threshold_Experimental)[0]
                filewriter.writerow([file, n, time_BF, time_DpR, time_seuil])
            