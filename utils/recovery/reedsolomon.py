import numpy as np

def create_reed_solomon_generator_matrix(k,n, field_size):
    """
    Create a Reed-Solomon generator matrix.
    Parameters:
        k: number of message symbols
        n: total number of symbols in the codeword
        field_size: size of the finite field (e.g., 256 for GF(2^8))
        Returns:
        generator_matrix: numpy array of shape (n, k) representing the generator matrix"""
    field = []
    for i in range(k):
        row = []
        for j in range(n):
            num = pow(j, i, field_size) 
            row.append(num)
        field.append(row)
    return np.array(field).T


def encode_message(message_bits, field_size=256):
    """
    Encode a bit string using Reed-Solomon codes.
    Parameters:
        message_bits: string of bits (e.g., "10110101")
        field_size: size of the finite field (default 256)
    Returns:
        encoded: list of encoded symbols
        k: number of message symbols (for decoding)
        n: total number of symbols in the codeword (for decoding)
    """
    # Pad message to make it divisible by 8
    while len(message_bits) % 8 != 0:
        message_bits += '0'
    
    # Split into 8-bit chunks and convert to integers
    message_symbols = []
    for i in range(0, len(message_bits), 8):
        chunk = message_bits[i:i+8]
        symbol = int(chunk, 2)
        message_symbols.append(symbol)
    
    # Automatically determine k and n
    k = len(message_symbols)
    n = k + max(2, k // 2)  # add at least 2 redundant symbols
    
    # Pad message symbols to length k (if needed)
    while len(message_symbols) < k:
        message_symbols.append(0)
    
    # Create generator matrix and encode
    G = create_reed_solomon_generator_matrix(k, n, field_size)
    message_vector = np.array(message_symbols[:k])
    encoded = np.dot(G, message_vector) % field_size
    
    return encoded.tolist()


def decode_message(encoded_symbols, field_size=256, original_bit_length=8):
    """
    Decode Reed-Solomon encoded symbols back to original bit string.
    Parameters:
        encoded_symbols: list of encoded symbols (use -1 for erasures)
        field_size: size of the finite field (default 256)
        original_bit_length: original length of bit string (for proper truncation)
    Returns:
        decoded_bits: original bit string
    """
    # Automatically calculate k and n from encoded symbols
    n = len(encoded_symbols)
    # Fix the k calculation to match the encoding ratio: n = k + k//2, so k = 2*n//3
    k = (2 * n) // 3
    if k == 0:  # Ensure k is at least 1
        k = 1
    
    G = create_reed_solomon_generator_matrix(k, n, field_size)
    
    # Decode the message
    # Handle erasures and errors automatically
    received_symbols = np.array(encoded_symbols)
    
    # Identify erasure positions (marked as -1)
    erasure_positions = np.where(received_symbols == -1)[0]
    
    # For erasures, we can decode directly using linear algebra
    if len(erasure_positions) > 0:
        # Replace erasures with zeros for calculation
        received_symbols[erasure_positions] = 0
        
        # Create syndrome matrix to detect errors
        syndrome = np.dot(G.T, received_symbols) % field_size
        
        # If syndrome is zero, no errors detected
        if np.all(syndrome == 0):
            decoded_symbols = received_symbols[:k]
        else:
            # Use Gaussian elimination to solve for erasures
            try:
                # Create system of equations for known positions
                known_positions = [i for i in range(n) if i not in erasure_positions]
                if len(known_positions) >= k:
                    A = G[known_positions[:k], :]
                    b = received_symbols[known_positions[:k]]
                    decoded_symbols = np.linalg.solve(A, b) % field_size
                else:
                    decoded_symbols = None
            except:
                decoded_symbols = None
    else:
        # No erasures, check for bit errors using syndrome decoding
        syndrome = np.dot(G.T, received_symbols) % field_size
        
        if np.all(syndrome == 0):
            # No errors detected
            decoded_symbols = received_symbols[:k]
        else:
            # Simple error correction: try single symbol errors
            decoded_symbols = None
            for error_pos in range(n):
                for error_val in range(1, field_size):
                    test_symbols = received_symbols.copy()
                    test_symbols[error_pos] = (test_symbols[error_pos] - error_val) % field_size
                    test_syndrome = np.dot(G.T, test_symbols) % field_size
                    
                    if np.all(test_syndrome == 0):
                        decoded_symbols = test_symbols[:k]
                        break
                if decoded_symbols is not None:
                    break
    
    if decoded_symbols is None:
        return None
    
    # Convert symbols back to bit string
    bit_string = ""
    for symbol in decoded_symbols:
        # Convert to 8-bit binary string
        bits = format(int(symbol), '08b')
        bit_string += bits
    
    # Truncate to original length if provided
    if original_bit_length:
        bit_string = bit_string[:original_bit_length]
    
    return bit_string



def encode_message_arbitrary(message_bitstring):
    # Store original length before padding
    original_length = len(message_bitstring)

    # Pad message to make it length 8
    while len(message_bitstring) % 8 != 0:
        message_bitstring += '0'

    pad_length = len(message_bitstring) - original_length

    symbols = [message_bitstring[i:i + 8] for i in range(0, len(message_bitstring), 8)]

    encoded_messages = []
    for symbol in symbols:
        encoded_messages.append(encode_message(symbol))

    return encoded_messages, pad_length


def decode_message_arbitrary(encoded_messages, pad_length):
    symbols = [decode_message(i) for i in encoded_messages]
    bit_string = ''.join(symbols)
    bit_string = bit_string[:len(bit_string)-pad_length]
    return bit_string






encoded, pad_length = encode_message_arbitrary("10110101011")
print("Encoded Symbols:", encoded)
print("Padding Length:", pad_length)


decoded = decode_message_arbitrary(encoded, pad_length)
print("Decoded Bit String:", decoded)
