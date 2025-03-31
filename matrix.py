# matrix.py
import numpy as np

class Matrix:
    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        if data is None:
            self.data = np.zeros((rows, cols))
        else:
            self.data = np.array(data).reshape((rows, cols))
    
    def randomize(self):
        self.data = np.random.uniform(-1, 1, (self.rows, self.cols))
    
    def dot(self, other):
        result = np.dot(self.data, other.data)
        return Matrix(result.shape[0], result.shape[1], result)
    
    def addBias(self):
        # Append a bias row (ones) at the bottom (assumes matrix is column vector)
        biased = np.vstack((self.data, np.ones((1, self.data.shape[1]))))
        return Matrix(biased.shape[0], biased.shape[1], biased)
    
    def activate(self, func=None):
        # Apply activation function elementwise. Default is sigmoid.
        if func is None:
            func = lambda x: 1/(1+np.exp(-x))
        activated = func(self.data)
        return Matrix(self.rows, self.cols, activated)
    
    def mutate(self, rate):
        mutation_mask = np.random.rand(self.rows, self.cols) < rate
        mutation_values = np.random.uniform(-1, 1, (self.rows, self.cols))
        self.data = np.where(mutation_mask, self.data + mutation_values, self.data)
    
    def toArray(self):
        return self.data.flatten().tolist()
    
    def clone(self):
        return Matrix(self.rows, self.cols, np.copy(self.data))
    
    def crossover(self, partner):
        child = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                child.data[i, j] = self.data[i, j] if np.random.rand() < 0.5 else partner.data[i, j]
        return child