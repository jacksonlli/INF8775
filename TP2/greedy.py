from utils import createBlocks, sortBySADecreasing
import sys
import numpy as np
import time

def greedy(blocks):#Select block with largest top surface area to place on tower
    sorted_block = sortBySADecreasing(blocks)
    index = 0
    while canPlaceBlock(sorted_block[index], sorted_block[index + 1]):#check if next block can be placed
        index+=1
    tower = sorted_block[0:index+1, 0:3]
    return sum(tower[:, 0]), tower

def canPlaceBlock(blockK, blockI):
    return blockK[1] < blockI[1] and blockK[2] < blockI[2]

def execute_greedy(blocks):
    start = time.time() 
    height, blockList = greedy(blocks)
    end = time.time()
    return end - start, height, blockList


