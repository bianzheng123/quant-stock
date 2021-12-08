import numpy as np
import torch

np.random.seed(2)

T = 20
L = 100
N = 10

x = np.empty((N, L), 'int64')
x[:] = np.array(range(L)) + np.random.randint(-4 * T, 4 * T, N).reshape(N, 1)
data = np.sin(x / 1.0 / T).astype('float64')
print(data.shape)
torch.save(data, open('traindata.pt', 'wb'))
