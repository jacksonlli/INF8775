import random
import math
import sys
import time
import csv
import os
from dynamic_programming import execute_dynamic_programming
from tabu import execute_tabu_search
from greedy import execute_greedy
from utils import createBlocks

ALGO = sys.argv[1] # Algo à utiliser vorace | progdyn | tabou
FILE = sys.argv[2] # Filepath 
MARKER1 = ""
MARKER2 = ""
if (len(sys.argv) >= 4):
    MARKER1 = sys.argv[3]
if (len(sys.argv) >= 5):
    MARKER2 = sys.argv[4] # -p or -t


def main(algo, filepath, marker1, marker2):

    blocks = createBlocks(filepath)
    if algo == "vorace":
        # Exécuter l'algorithme Diviser pour régner
        time_elapsed, height, tower = greedy(blocks)
        if (marker1 == 'p' or marker2 == 'p'):
            for block in tower:
                print(block)
        if (marker1 == 't' or marker2 == 't'):
            print('Time: ', time_elapsed*1000)#assignment asks for time in ms
        print('Maximum Tower Height: ', height)
    
    elif algo == "progdyn":
        # Exécuter l'algorithme Diviser pour régner
        time_elapsed, height, tower = execute_dynamic_programming(blocks)
        if (marker1 == 'p' or marker2 == 'p'):
            for block in tower:
                print(block)
        if (marker1 == 't' or marker2 == 't'):
            print('Time: ', time_elapsed*1000)#assignment asks for time in ms
        print('Maximum Tower Height: ', height)
            
        
    elif algo == "tabou":
        # Exécuter l'algorithme Diviser pour régner
        time_elapsed, height, tower = execute_tabu_search(blocks)
        if (marker1 == 'p' or marker2 == 'p'):
            for block in tower:
                print(block)
        if (marker1 == 't' or marker2 == 't'):
            print('Time: ', time_elapsed*1000)#assignment asks for time in ms
        print('Maximum Tower Height: ', height)
            
main(ALGO, FILE, MARKER1, MARKER2)

