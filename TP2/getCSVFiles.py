import csv
from utils import createBlocks
from dynamic_programming import execute_dynamic_programming
from tabu import execute_tabu_search
from greedy import execute_greedy
import os

#runs the all three algorithms on all testsets and writes everything into a csv file.

test_directory = "gen_files"

with open('dataTaboo50000.csv', 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Sample','Sample Size','Vorace Time', 'ProgDyn Time', 'Tabou Time', 'Vorace Height', 'ProgDyn Height', 'Tabou Height'])
    
    for n in sorted(os.listdir(test_directory), key=len):
        path = os.path.join(test_directory,str(n))
        if not n=="50000": 
            continue
        for file in os.listdir(path):
            print("---------------------")
            print("File: ", file)
            blocks = createBlocks(os.path.join(path, file))
            time_V, height_V, tower =  (-1, -1, [])#execute_greedy(blocks)
            time_DP, height_DP, tower = (-1, -1, [])#execute_dynamic_programming(blocks)
            time_T, height_T, tower = execute_tabu_search(blocks)
            print("Time: ", time_T)
            filewriter.writerow([file, blocks.shape[0], time_V, time_DP, time_T, height_V, height_DP, height_T])
            break