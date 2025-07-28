import numpy as np
def create_message(symbols, C):
    return np.repeat(symbols, C)

def decode_message(message, C):
    return np.mean(message.reshape(-1, C), axis=1)

