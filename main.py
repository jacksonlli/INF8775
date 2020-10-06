import random
import math
import sys
import time
import csv

from brute_force import execute_brute_force
from DpR import execute_DpR
from utils import GRID_SIZE, getPointsfromFile

ALGO = sys.argv[1] # Algo à utiliser DPR ou BF
FILE = sys.argv[2] # Filepath


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

def main(algo, filepath):
    POINTS = getPointsfromFile(filepath)
    sorted_points_x = sorted(POINTS, key=lambda x: x[0])
    sorted_points_y = sorted(POINTS, key=lambda x: x[1])
    
    if algo == "BF":
        # Exécuter l'algorithme force brute
        time_BF, dist_BF, points_BF = execute_brute_force(sorted_points_x)
        print("Time : ", time_BF)
        print("Minimum distance : ", dist_BF)
        print("Corresponding Points: ", points_BF)
    
    elif algo == "DPR":
        # Exécuter l'algorithme Diviser pour régner
        SEUIL_DPR = 3
        time_DPR, dist_DPR, points_DPR = execute_DpR(sorted_points_x, sorted_points_y, SEUIL_DPR)
        print("Time : ", time_DPR)
        print("Minimum distance : ", dist_DPR)
        print("Corresponding Points: ", points_DPR)
        
main(ALGO, FILE)