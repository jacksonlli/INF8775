import random
import math
import sys
import time
import csv
import os
from dynamic_programming import execute_dynamic_programming
from utils import createBlocks

ALGO = sys.argv[1] # Algo à utiliser vorace | progdyn | tabou
FILE = sys.argv[2] # Filepath 
if (len(sys.argv) < 4):
    MARKER = ""
else:
    MARKER = sys.argv[3] # -p or -t


def main(algo, filepath, marker):

    blocks = createBlocks(filepath)
    if algo == "vorace":
        # Exécuter l'algorithme Diviser pour régner
        time_elapsed, height, tower = vorace(blocks)
        if (marker == 'p'):
            for block in tower:
                print(block)
        elif (marker == 't'):
            print('Time: ', time_elapsed*1000)#assignment asks for time in ms
        print('Maximum Tower Height: ', height)
    
    elif algo == "progdyn":
        # Exécuter l'algorithme Diviser pour régner
        time_elapsed, height, tower = execute_dynamic_programming(blocks)
        if (marker == 'p'):
            for block in tower:
                print(block)
        elif (marker == 't'):
            print('Time: ', time_elapsed*1000)#assignment asks for time in ms
        print('Maximum Tower Height: ', height)
            
        
    elif algo == "tabou":
        # Exécuter l'algorithme Diviser pour régner
        time_elapsed, height, tower = execute_tabu_search(blocks)
        if (marker == 'p'):
            for block in tower:
                print(block)
        elif (marker == 't'):
            print('Time: ', time_elapsed*1000)#assignment asks for time in ms
        print('Maximum Tower Height: ', height)
            
main(ALGO, FILE, MARKER)

