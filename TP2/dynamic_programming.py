from utils import createBlocks, sortBySAIncreasing
import sys
import numpy as np
import time

FILEPATH = sys.argv[1]

def dyn_prog(blocks, n):#n in this case is actually 3N, where N is the number of unique blocks
    sorted_blocks = sortBySAIncreasing(blocks)#sorted in increasing surface area
    h_tower = np.copy(sorted_blocks[:, 0]) #tableau de calculs for dynamic programming, initialised with block height
    pointers = [None] * n #refers to index of the block on top of the sub-tower
    isTerminated = [False] * n #terminated blocks have reached their optimal subsolution 
    inn = 0
    while False in isTerminated:# at most n/3 - 1 iterations
        print(inn)
        inn += 1
        for k in range(n): #k is the index of the current block to be placed on top
            if not isTerminated[k]:
                canStillBePlaced = False
                for i in range(k+1,n): #i is the index of the top block of a subtower on which we place k
                    if not isTerminated[i] and canPlaceBlock(sorted_blocks[k], sorted_blocks[i]):
                        if worthPlacingBlock(sorted_blocks[k, 0], h_tower[i], h_tower[k]) and not blockAlreadyInTower(sorted_blocks[:, 3], pointers, k, i):
                            h_tower[k] = sorted_blocks[k, 0] + h_tower[i]
                            pointers[k] = i
                        canStillBePlaced = True
                if not canStillBePlaced:
                    isTerminated[k] = True
    index_max = np.argmax(h_tower)
    return h_tower[index_max], getBlocksInTower(sorted_blocks[:, 0:3], pointers, index_max)
    
def canPlaceBlock(blockK, blockI):
    return blockK[1] < blockI[1] and blockK[2] < blockI[2]

def worthPlacingBlock(block_height, subtower_height, current_tower_height):
    return block_height + subtower_height > current_tower_height

def blockAlreadyInTower(all_IDs, pointers, block_index, tower_top_block_index):#max recursion of n/3 - 1 since tower will have a maximum height of n/3 (the number of unique blocks N)
    block_ID = all_IDs[block_index]
    top_block_ID = all_IDs[tower_top_block_index]
    if block_ID == top_block_ID:
        return True
    elif pointers[tower_top_block_index] == None:
        return False
    else:
        return False or blockAlreadyInTower(all_IDs, pointers, block_index, pointers[tower_top_block_index]) 
    
def getBlocksInTower(block_Dims, pointers, top_block_index):#should be exactly N or n/3 iterations
    current_Block_Dims = block_Dims[top_block_index]
    if pointers[top_block_index] == None:
        return [[current_Block_Dims[0], current_Block_Dims[1], current_Block_Dims[2]]]
    return getBlocksInTower(block_Dims, pointers, pointers[top_block_index]) + [[current_Block_Dims[0], current_Block_Dims[1], current_Block_Dims[2]]]

def execute_dynamic_programming(blocks, n):
    start = time.time() 
    height, blockList = dyn_prog(blocks, n)
    end = time.time()
    return end - start, height, blockList

blocks, n = createBlocks(FILEPATH)
t, h, l = execute_dynamic_programming(blocks, n)
print(t)


