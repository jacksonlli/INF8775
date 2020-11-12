from utils import createBlocks, sortBySADecreasing
import sys
import numpy as np
import time

def greedy(blocks):#Select block with largest top surface area to place on tower
    sorted_block = sortBySADecreasing(blocks)
    n = sorted_block.shape[0]
    tower = [[sorted_block[0, 0], sorted_block[0, 1], sorted_block[0, 2]]]
    for index in range(1, n):
        if canPlaceBlock(sorted_block[index], tower[-1]):#check if next block can be placed
            tower = tower + [[sorted_block[index, 0], sorted_block[index, 1], sorted_block[index, 2]]]
    return sum(row[0] for row in tower), tower

def canPlaceBlock(blockK, blockI):#try to place k on i
    return blockK[1] < blockI[1] and blockK[2] < blockI[2]

def execute_greedy(blocks):
    start = time.time() 
    height, blockList = greedy(blocks)
    end = time.time()
    return end - start, height, blockList


