import timeit

import numpy as np


arr = np.array([10,20,30,40,50])
arr2 =  np.array([10,20,30,40,50,50,60])

g = np.add(arr,arr2)
print(g)