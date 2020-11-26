import sys
import os
import math

FILEPATH = sys.argv[1]

def createMuniField(path):  # creates a 2d-list of municipalities [y,x] 
				# that is y rows by x columns
	with open(path,"r") as infile:
		xy = infile.readline().split(" ")
		x = int(xy[0])
		y = int(xy[1])
		field = [[0] * x for i in range(y)]
		for j in range(y):
			row = infile.readline().split("  ")
			for k in range(x):
				field[j][k] = int(row[k])
	return field,x,y

def manDist(x1,y1,x2,y2):
	return (abs(x1 - x2) + abs(y1-y2))

field,x,y = createMuniField(FILEPATH)
print(field)