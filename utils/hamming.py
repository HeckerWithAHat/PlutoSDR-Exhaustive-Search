import numpy as np
def create_hamming_code_matrices(r):
    G = np.zeros((2**r-r-1,2**r-1)) 
    H = np.zeros((r,2**r-1)) 
    n = 2**r - 1  
    k = n - r    
    for i in range(1, n + 1):
        binary_rep = format(i, f'0{r}b')
        for j in range(r):
            H[j, i-1] = int(binary_rep[j])
    for i in range(k):
        G[i, i] = 1
    parity_positions = [2**i - 1 for i in range(r)] 
    info_col = 0
    for col in range(n):
        if col not in parity_positions:
            for row in range(r):
                G[info_col, col] = H[row, col]
            info_col += 1
    return G.astype(int), H.astype(int)
    
def hamming_decode(codeword, H):
    codeword = np.array(codeword)
    syndrome = np.dot(H, codeword) % 2
    if np.all(syndrome == 0):
        return codeword
    error_position = None
    for i in range(H.shape[1]):
        if np.array_equal(syndrome, H[:, i]):
            error_position = i
            break
    if error_position is not None:
        corrected_codeword = codeword.copy()
        corrected_codeword[error_position] = 1 - corrected_codeword[error_position]
        return corrected_codeword
    return codeword