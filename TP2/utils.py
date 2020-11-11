import sys
import os

import numpy as np

FILEPATH = sys.argv[1]


def createBlocks(path):
	# path is a string containing absolute path from 
	# Isolate the sample size from the path string
	part = path.split("b")
	n_strings = part.pop().split("_")
	n = int(n_strings[0])
	# numLines represents expected length of text file
	numLines = 3*n

	# Instantiate blocks array with:
	# B = numLines x { h | l | p | ID | SurfaceArea }
	blocks = np.zeros((numLines,5),dtype=int)
	with open(path,"r") as infile:
		for i in range(numLines):
			# store h,l,p as first three entries
			hlp = infile.readline().split(" ")
			blocks[i,0], blocks[i,1], blocks[i,2] = int(hlp[0]),int(hlp[1]),int(hlp[2])
			# fourth entry is ID (numLines floor divided by 3)
			blocks[i,3] = int(i//3)
			#fifth entry is Surface Area
			blocks[i,4] = (blocks[i][1]*blocks[i][2])
	return blocks
    
def printBlocks(Blocks):
	for i in range(Blocks.shape[0]):
		print("Dimensions of block ", i, " for each orientation:")
		print ("h: ", Blocks[i,0], ", l: ", Blocks[i,1], ", p: ", Blocks[i,2],", ID: ", Blocks[i,3],", Surface Area: ", Blocks[i,4])

def sortBySA(blocks):
    inc=np.argsort(blocks[:,4])#indexes of rows sorted according to last column in increasing order
    dec = inc[::-1]#now in decreasing order
    sorted_blocks=blocks[dec]#reorganise list according to "dec" indexes
    return sorted_blocks
    
# def main(filepath):

	# Blocks = createBlocks(filepath)
	# printBlocks(Blocks)
	

# main(FILEPATH)
	
	
		