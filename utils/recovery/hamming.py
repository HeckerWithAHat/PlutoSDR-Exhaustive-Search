import numpy as np
def create_hamming_code_matrices(r):
    """
    Parameters:
        r - Number of parity bits
    Returns:
        G - Generator matrix
        H - Parity-check matrix
    """
    n = 2**r - 1  
    k = n - r    
    
    # Create H matrix with identity matrix first, then parity columns
    H = np.zeros((r, n))
    
    # Set identity matrix in the first r columns
    for i in range(r):
        H[i, i] = 1
    
    # Fill remaining columns with binary representations
    col_idx = r
    for i in range(1, n + 1):
        binary_rep = format(i, f'0{r}b')
        # Skip positions that would create all-zero or identity columns
        if i != 2**0 and i != 2**1 and i != 2**2 and (r < 4 or i != 2**3) and (r < 5 or i != 2**4):
            for j in range(r):
                H[j, col_idx] = int(binary_rep[j])
            col_idx += 1
            if col_idx >= n:
                break
    
    # Create G matrix in systematic form [I_k | P]
    G = np.zeros((k, n))
    
    # Identity matrix for information bits (last k columns)
    for i in range(k):
        G[i, r + i] = 1
    
    # Parity part (first r columns) - transpose of the parity part of H
    for i in range(k):
        for j in range(r):
            G[i, j] = H[j, r + i]
    
    return G.astype(int), H.astype(int)
    
def hamming_decode(codeword, H, padding_count):
    """
    Decode a full Hamming-encoded stream and correct single-bit errors in each codeword block.
    Parameters:
        codeword: numpy array or list of bits (entire encoded stream)
        H: Parity-check matrix
        padding_count: Number of padding bits at the end of the original message
    Returns:
        Decoded and corrected original message bits as a list
    """
    codeword = np.array(list(map(int, list(codeword))))
    n = H.shape[1]
    r = H.shape[0]
    k = n - r

    corrected_bits = []

    for i in range(0, len(codeword), n):
        block = codeword[i:i+n]
        if len(block) < n:
            break  # Skip incomplete blocks at end (shouldn't occur unless input is malformed)

        H_trans = H.T
        syndrome = np.dot(block, H_trans) % 2

        # If syndrome is zero, no error
        if not np.any(syndrome):
            corrected_block = block
        else:
            # Find the position of the error
            error_position = None
            for j in range(n):
                if np.array_equal(H[:, j], syndrome):
                    error_position = j
                    break
            corrected_block = block.copy()
            if error_position is not None:
                corrected_block[error_position] ^= 1  # Flip the bit

        corrected_bits.extend(corrected_block[r:])

    # Remove padding
    if padding_count > 0:
        corrected_bits = corrected_bits[:-padding_count]

    return corrected_bits





def encode_bitstring_hamming(bitstring):
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

    r = 0
    while (2 ** r) < (len(bits) + r + 1):
        r += 1
    
    # Calculate Hamming code parameters
    n = 2**r - 1  # Code length
    k = n - r     # Information bits per codeword
    print(f"Using Hamming code with r={r}, n={n}, k={k}")
    # Create generator matrix
    G, H = create_hamming_code_matrices(r)
    
    # Pad the bitstring if necessary to make it divisible by k
    padding_count = k - (len(bits) % k)
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

    return [encoded_bits, H, padding_count]


