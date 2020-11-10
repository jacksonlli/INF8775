import sys
import os

import numpy as np

filepath = sys.argv[1]

def createBlocks(path):
	part = path.split("b")
	n_strings = part.pop().split("_")
	n = int(n_strings[0])
	numLines = 3*n
	with open(path,"r") as infile:
		Blocks = np.zeros((n,3,3))
		for i in range(n):
			for j in range(3):
				dimArr = np.array([int(x) for x in infile.readline().split()])
				Blocks[i][j] = dimArr

	return Blocks
def printBlocks(Blocks):
	for i in range(Blocks.shape[0]):
		print("Dimensions of block ", i, " for each orientation:")
		for j in range(3):
			print ("h: ", Blocks[i][j][0], ", l: ", Blocks[i][j][1], ", p: ", Blocks[i][j][2])

def findSA(Blocks):
	SA = np.zeros([Blocks.shape[0], 3])
	for i in range(Blocks.shape[0]):
		for j in range(3):
			SA[i][j] = Blocks[i][j][1] * Blocks[i][j][2]
	return SA	

def main(filepath):

	Blocks = createBlocks(filepath)
	surfaceAreaArr = findSA(Blocks)
	print(surfaceAreaArr)

main(filepath)
	
	
		