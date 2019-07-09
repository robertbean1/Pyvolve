import numpy as np

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))

def sigmoid(x):
    return 1 / ( 1 + np.exp(-x) )

def tanh(x):
    return ( np.exp(x) - np.exp(-x) ) / ( np.exp(x) + np.exp(-x) )

def softplus(x):
    return np.log(1 + np.exp(x))

def relu(x):
    x = np.array(x)
    return np.maximum(x, 0, x)

def get_activation(func):
    if isinstance(func, str):
        if func == 'relu':
            return relu
        if func == 'softplus':
            return softplus
        if func == 'tanh':
            return tanh
        if func == 'sigmoid':
            return sigmoid
        if func == 'softmax':
            return softmax

    else:
        return func
