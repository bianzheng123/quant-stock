import numpy as np

arr = np.array([[2, 1], [3, 5]])
print(arr.std(axis=0), arr.std(axis=1))