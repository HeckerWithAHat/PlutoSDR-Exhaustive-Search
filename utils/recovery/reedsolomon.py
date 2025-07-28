import numpy as np

def create_reed_solomon_generator_matrix(k,n, field_size):
    field = []
    for i in range(k):
        row = []
        for j in range(n):
            num = pow(j, i, field_size) 
            row.append(num)
        field.append(row)
    return np.array(field)

def decode_rs_erasure(received, G, field_size):
    received = np.array(received)
    known_indices = np.where(received != -1)[0]
    y = received[known_indices]
    G_sub = G[:, known_indices].T
    if G_sub.shape[0] < G_sub.shape[1]:
        return None
    def modinv(a, mod):
        return pow(int(a), -1, mod)
    A = G_sub.copy().astype(int)
    b = y.copy().astype(int)
    k = A.shape[1]
    for i in range(k):
        for r in range(i, A.shape[0]):
            if A[r, i] % field_size != 0:
                break
        else:
            return None
        if r != i:
            A[[i, r]] = A[[r, i]]
            b[[i, r]] = b[[r, i]]
        inv = modinv(A[i, i], field_size)
        A[i] = (A[i] * inv) % field_size
        b[i] = (b[i] * inv) % field_size
        for j in range(A.shape[0]):
            if j != i and A[j, i] != 0:
                factor = A[j, i]
                A[j] = (A[j] - factor * A[i]) % field_size
                b[j] = (b[j] - factor * b[i]) % field_size
    return b[:k] % field_size