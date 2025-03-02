import timeit

import numpy as np

arr = np.array([10, 20, 30, 40, 50])
arr2 = np.array([10, 20, 30, 40, 50, 50, 60])

# Create a 0D Array
arr0 = np.array(24)
print('0D array is', arr0)
# Create a 1D Array
arr1 = np.array([1, 2, 3, 4])
print('1D array is', arr1)
# Create a 2D Array
arr2 = np.array([[1, 1, 1], [1, 2, 1]])
print('2D array is', arr2)
# Create a 3D Array
arr3 = np.array([[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]])
print('3D array is', arr3)
# Create a 4D Array
arr4 = np.array([[[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]], [[[5, 5, 5], [6, 6, 6]], [[7, 7, 7], [8, 8, 8]]]])
print('4D array is', arr4)
