import numpy as np
def create_hamming_code_matrices(r):
    """
    Parameters:
        r - Number of parity bits
    Returns:
        G - Generator matrix
        H - Parity-check matrix
    """
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




def encode_bitstring_hamming(bitstring, r=3):
    """
    Encode a bit string using Hamming code with parameter r.
    
    Parameters:
    bitstring: string of '0's and '1's or list/array of bits
    r: Hamming code parameter (number of parity bits)
    
    Returns:
    encoded_bitstring: list of encoded bits
    """
    # Convert string to list of integers if needed
    if isinstance(bitstring, str):
        bits = [int(b) for b in bitstring]
    else:
        bits = list(bitstring)
    
    # Calculate Hamming code parameters
    n = 2**r - 1  # Code length
    k = n - r     # Information bits per codeword
    
    # Create generator matrix
    G, _ = create_hamming_code_matrices(r)
    
    # Pad the bitstring if necessary to make it divisible by k
    while len(bits) % k != 0:
        bits.append(0)
    
    encoded_bits = []
    
    # Encode each block of k bits
    for i in range(0, len(bits), k):
        # Extract k-bit block
        block = np.array(bits[i:i+k])
        
        # Encode using generator matrix
        encoded_block = np.dot(block, G) % 2
        
        # Add to result
        encoded_bits.extend(encoded_block.tolist())
    
    return encoded_bits