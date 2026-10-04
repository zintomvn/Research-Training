import numpy as np
test = np.array([1,0,0,0,1])
pred = np.array([0,0,0,0,0])

accuracy = np.sum(test==pred) / test.shape[0]
print(accuracy)