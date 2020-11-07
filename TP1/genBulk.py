#generates testsets in bulk
import random
import sys
import os

n = -1
fn = ''

n = int(sys.argv[1]) #sample size
k = int(sys.argv[2]) #number of files to generate
c = 1000000

test_directory = "testsets_small"

path = os.path.join(test_directory,str(n))
if not os.path.isdir(path):
    os.mkdir(path)

for i in range(k):
    fn = os.path.join(test_directory, str(n), "testset_"+str(n)+"_"+str(i+1)+".txt")
    points = [[random.randint(0, c), random.randint(0, c)] for _ in range(n)]

    with open(fn, 'w') as f:
        f.write(str(n) + '\n')
        for i in range(n):
            f.write(str(points[i][0]) + ' ' + str(points[i][1]) + '\n')
    f.close()
