from utils import createBlocks, sortBySA
import sys
import numpy as np

FILEPATH = sys.argv[1]

def execute_dynamic_programming(sorted_blocks):
    for i in range(3):
        print(sorted_blocks[i,4])
	
blocks = createBlocks(FILEPATH)
sorted_blocks = sortBySA(blocks)
execute_dynamic_programming(sorted_blocks)
