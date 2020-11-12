import csv
from utils import createBlocks
from dynamic_programming import execute_dynamic_programming
import os

#runs the all three algorithms on all testsets and writes everything into a csv file.

test_directory = "gen_files"

with open('data.csv', 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Sample','Sample Size','Vorace', 'ProgDyn', 'Tabou'])
    for n in sorted(os.listdir(test_directory), key=len):
        path = os.path.join(test_directory,str(n))
        for file in os.listdir(path):
            print(file)
            blocks = createBlocks(os.path.join(path, file))
            time_V = -1
            time_DP = execute_dynamic_programming(blocks)[0]
            time_T = -1
            filewriter.writerow([file, blocks.shape[0], time_V, time_DP, time_T])