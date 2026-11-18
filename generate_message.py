
import numpy as np

def get_qam_constellation():
    """
    Generate an M-QAM constellation with Gray coding.

    Parameters:
    M (int): Modulation order (must be a perfect square).
    Es (float): Symbol energy normalization factor (default is 1).

    Returns:
    np.ndarray: Array of M-QAM constellation points following Gray coding.
    """

    # Function to convert binary to Gray code
    def binary_to_gray(n):
        return n ^ (n >> 1)

    # Generate Gray-coded indices for both axes
    gray_indices = np.array([binary_to_gray(i) for i in range(16)])

    # Normalize Gray-coded indices to constellation points
    re_gray = 2 * gray_indices - (16 - 1)  # Shift and scale
    im_gray = 2 * gray_indices - (16 - 1)

    # Create the constellation using Gray-coded indices
    const = np.array(
        [complex(re, -im) for im in im_gray for re in re_gray]
    )  # Flip imag for correct quadrant

    # Normalize to unit average energy Es
    const = const / np.sqrt(np.mean(np.abs(const) ** 2)) * np.sqrt(1)

    const2d = const.reshape((16, 16))



    constellation_mapping = {}
    for i in range(16):
        for j in range(16):
            bitstring = bin(gray_indices[i])[2:].zfill(4) + bin(gray_indices[j])[2:].zfill(4)
            constellation_mapping[bitstring] = const2d[i, j]

    return constellation_mapping

   


def generate_message(text: str):
    """
    Simulates the compression and recovery process with the given parameters.
    
    Parameters:
        Compression - Enum value for compression method
        Recovery - Enum value for recovery method
        Constellation - Enum value for constellation size
        SymbolErrorProbability - Enum value for symbol error probability
        Repitition - Enum value for repetition factor
        filepath - Name of the file to save results
    """

    bitstring = ''.join(format(byte, '08b') for byte in bytearray(text.encode('utf-8')))
    print("Original Bitstring:", bitstring)
    bytestring_array = [bitstring[i:i+8] for i in range(0, len(bitstring), 8)]
    const = get_qam_constellation()
    modulated_signal = [const[bits] for bits in bytestring_array]
    print("Modulated Signal:", modulated_signal)


generate_message("flag{M3rryChr1stm4s}")