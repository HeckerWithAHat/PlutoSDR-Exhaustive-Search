import numpy as np
def digital_modulation(bits, M):
    """
    Parameters:
        bits - bitstring to convert to a symbol array
        M - Length of Constellation/How many possible symbols
    """
    if M > 0 and (M & (M - 1)) == 0:
        pass
    else:
        raise ValueError("M is not a Power of 2")

    L = np.log2(M).astype(int) 
    
    constellation = [i for i in range(-1*int(M - 1), M, 2)]

    
    symbols = []
    
    for i in range(0, len(bits), L):
        startIndex = i
        endIndex = i + L

        binary = bits[startIndex:endIndex]

        symbol_idx = 0
        for bit in binary:
            symbol_idx = (symbol_idx << 1) | int(bit)
        
        mapped = constellation[symbol_idx]

        symbols.append(mapped)

    return symbols


def digital_demodulation(symbols, M):
    """
    Parameters:
        symbols - array of symbols to convert back to bits
        M - Length of Constellation/How many possible symbols
    """
    if M > 0 and (M & (M - 1)) == 0:
        pass
    else:
        raise ValueError("M is not a Power of 2")

    L = np.log2(M).astype(int)
    
    constellation = [i for i in range(-1*int(M - 1), M, 2)]
    
    bits = ""
    
    for symbol in symbols:
        symbol_idx = constellation.index(symbol)
        print(L)
        binary = bin(symbol_idx)[2:].zfill(L) # bin converts to 0b and then some binary string, 2: removed the 0b, zfill pads it
        bits += binary
    
    return bits


encoded = digital_modulation("101010101010101010101011101010101010101010101011", 16)

decoded = digital_demodulation(encoded, 16)

print("Decoded correctly: ", "101010101010101010101011101010101010101010101011" == decoded)