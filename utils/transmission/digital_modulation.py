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
    constellation = [i for i in range(-int(M - 1), int(M), 2)]
    print("Constellation:", constellation)
    
    symbols = []
    print(len(bits[0]))
    for i in range(0, len(bits[0]), L):
        startIndex = i
        endIndex = i + L
        binary = bits[0][startIndex:endIndex]
        symbol_idx = 0
        
        for bit in binary:
            symbol_idx = (symbol_idx << 1) | int(bit)
            
        
        mapped = constellation[symbol_idx]

        symbols.append(mapped)
    print("Symbols:", symbols)

    return [symbols, M]


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
        binary = bin(symbol_idx)[2:].zfill(L) # bin converts to 0b and then some binary string, 2: removed the 0b, zfill pads it
        bits += binary
    
    return bits







# print(digital_modulation("10101000100101010001001000", 8))