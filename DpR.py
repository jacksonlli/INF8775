import sys
import time
from utils import MAX_DIST, distance

from brute_force import brute_force
sys.setrecursionlimit(1500)


def find_min_strip(points_y, d):
    strip_min = d
    min_points = []
    l = len(points_y)
    for pos, pt1 in enumerate(points_y):
        for pt2 in points_y[(pos+1):(min(l, pos+7))]:
            dist = distance(pt1, pt2)
            if dist < strip_min:
                strip_min = dist
                min_points = [pt1, pt2]
    return strip_min, min_points



'''
Algorithme Diviser pour Régner pour résoudre le problème.
Un point est représenté par un typle (position_x, position_y).
Les coordonnées des points sont compris entre 0 et 1,000,000.
points_x contient la liste des points triés sur l'axe des abscisses.
points_y contient la liste des points triés sur l'axe des ordonnées.
seuil_recur est le seuil à partir duquel on utilie l'algo force brute.
'''
def DpR(points_x, points_y, seuil_recur):
    nb_points = len(points_x)

    # Si le nombre de points est inférieur au seuil de récursivité, on change 
    # d'algorithme pour trouver la plus petite distance
    if nb_points <= seuil_recur:
        min_dist, min_points = brute_force(points_x)
        return min_dist, min_points

    # On divise nos points en deux groupes, en fonction de leur abscisse
    # puis on cherche récursivement le minimum dans chaque groupe
    middle = nb_points // 2
    left_group_x = points_x[:middle]
    right_group_x = points_x[middle:]
    
    # middle_x correspond à l'abscisse du premier point du groupe de droite
    middle_x = points_x[middle][0]

    # On sépare la liste triée selon y en deux groupes également
    left_group_y = []
    right_group_y = []
    for p in points_y:
        if p[0] < middle_x:
            left_group_y.append(p)
        else:
            right_group_y.append(p)

    # On appelle récursivement l'algo Diviser pour Régner
    min_dist_left, min_left_points = DpR(left_group_x, left_group_y, seuil_recur)
    min_dist_right, min_right_points = DpR(right_group_x, right_group_y, seuil_recur)
    if min_dist_left < min_dist_right:
        d = min_dist_left
        min_points = min_left_points
    else:
        d = min_dist_right
        min_points = min_right_points
    
    # On construit une bande verticale dans laquelle les points ont une abscisse à moins
    # d'une distance d de middle_x à gauche et à droite (d = distance minimale trouvée
    # dans le groupe de gauche et dans le groupe de droite)
    strip = [p for p in points_y if abs(p[0] - middle_x) < d]
    min_strip, strip_points = find_min_strip(strip, d)
    if min_strip < d:
        min_dist = min_strip
        min_points = strip_points
    else:
        min_dist = d

    return min_dist, min_points

def execute_DpR(sorted_points_x, sorted_points_y, seuil_recur):
    start = time.time()
    min_dist_dpr, min_points_dpr = DpR(sorted_points_x, sorted_points_y, seuil_recur)
    end = time.time()
    # print("DPR: ", min_dpr)
    return end - start, min_dist_dpr, min_points_dpr