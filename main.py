import random
import math
import sys
import time
import csv
import os

from brute_force import execute_brute_force
from DpR import execute_DpR
from utils import GRID_SIZE, threshold_Experimental, threshold_Arbitrary, getPointsfromFile

ALGO = sys.argv[1] # Algo à utiliser brute, recursif (avec seuil arbitraire) ou seuil (recursif avec seuil experimental)
FILE = sys.argv[2] # Filepath 
if (len(sys.argv) < 4):
    MARKER = ""
else:
    MARKER = sys.argv[3] # -p or -t

    

'''
Un point est représenté par un tuple (position_x, position_y)
La fonction generate_points génère une liste de N points.
'''
def generate_points(N):
    points = [(random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE)) for i in range(N)]
    return points

'''
--------------------------------------------------------------------
ATTENTION : Dans votre code vous devez utiliser le générateur gen.py
pour générer des points. Vous devez donc modifier ce code pour importer
les points depuis les fichiers générés.
De plus, vous devez faire en sorte que l'interface du tp.sh soit
compatible avec ce code (par exemple l'utilisation de flag -e, -a, (p et -t)).
--------------------------------------------------------------------
 '''

def main(algo, filepath, marker):

    POINTS = getPointsfromFile(filepath)
    sorted_points_x = sorted(POINTS, key=lambda x: x[0])
    sorted_points_y = sorted(POINTS, key=lambda x: x[1])
    
    if algo == "brute":
        # Exécuter l'algorithme force brute
        time_BF, dist_BF, points_BF = execute_brute_force(sorted_points_x)
        if (marker == 'p'):
            print("Minimum distance : ", dist_BF)
        elif (marker == 't'):
            print("Time : ", time_BF)
        else:
            print("Time : ", time_BF)
            print("Minimum distance : ", dist_BF)
            print("Solution Points: ", points_BF)
    
    elif algo == "recursif":
        # Exécuter l'algorithme Diviser pour régner
        SEUIL_DPR = threshold_Arbitrary
        time_DPR, dist_DPR, points_DPR = execute_DpR(sorted_points_x, sorted_points_y, SEUIL_DPR)
        if (marker == 'p'):
            print("Minimum distance : ", dist_DPR)
        elif (marker == 't'):
            print("Time : ", time_DPR)
        else:
            print("Time : ", time_DPR)
            print("Minimum distance : ", dist_DPR)
            print("Solution Points: ", points_DPR)
        
    elif algo == "seuil":
        # Exécuter l'algorithme Diviser pour régner avec seuil de recursivite experimental
        SEUIL_DPR = threshold_Experimental
        time_DPR, dist_DPR, points_DPR = execute_DpR(sorted_points_x, sorted_points_y, SEUIL_DPR)
        if (marker == 'p'):
            print("Minimum distance : ", dist_DPR)
        elif (marker == 't'):
            print("Time : ", time_DPR)
        else:
            print("Time : ", time_DPR)
            print("Minimum distance : ", dist_DPR)
            print("Solution Points: ", points_DPR)
            
main(ALGO, FILE, MARKER)

