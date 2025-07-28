from utils.recovery.hamming import encode_bitstring_hamming
from utils.recovery.hamming import hamming_decode

from utils.compression.huffman import huffman_encoding
from utils.compression.huffman import huffman_decoding

from utils.compression.lempelziv import lempel_ziv_encoding
from utils.compression.lempelziv import lempel_ziv_decoding

from utils.recovery.reedsolomon import create_reed_solomon_generator_matrix
from utils.recovery.reedsolomon import decode_rs_erasure

from utils.recovery.repitition import repetition_encode
from utils.recovery.repitition import repetition_decode

from utils.transmission.digital_modulation import digital_modulation
from utils.transmission.digital_modulation import digital_demodulation

from utils.transmission.create_message import create_message
from utils.transmission.create_message import decode_message

from enum import Enum
import numpy as np
import sys

class Compression(Enum):
    HUFFMAN = (huffman_encoding, huffman_decoding)
    LEMPEL_ZIV = (lempel_ziv_encoding, lempel_ziv_decoding)

class Recovery(Enum):
    HAMMING = (encode_bitstring_hamming, hamming_decode)
    REED_SOLOMON = (create_reed_solomon_generator_matrix, decode_rs_erasure)
    REPETITION = (repetition_encode, repetition_decode)

class Constellation(Enum):
    QAM2 = 2
    QAM4 = 4
    QAM8 = 8
    QAM16 = 16


class SymbolErrorProbability(Enum):
    P0 = 0.01
    P1 = 0.001
    P2 = 0.0001
    P3 = 0.00001
    P4 = 0.000001

class Repitition(Enum):
    R1 = 2
    R2 = 4
    R3 = 8
    R4 = 16



def simulate(Compression: Compression, Recovery: Recovery, Constellation: Constellation, SymbolErrorProbability: SymbolErrorProbability, Repitition: Repitition, filepath: str):
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
    bitstring = ""
    try:
        with open(filepath, "rb") as f:
            content = f.read()  # Read the entire file content as bytes
            bitstring = "".join(f"{byte:08b}" for byte in content)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    print(f"Bitstring: {bitstring}")
    # Compression
    compressed_bits, compression_data = Compression.value[0](bitstring)
    print(f"Compressed Bits: {compressed_bits}")
    # Recovery
    recovery_added_bits = Recovery.value[0](compressed_bits)
    print(f"Recovery Added Bits: {recovery_added_bits}")
    # Modulation
    symbols = digital_modulation(recovery_added_bits, Constellation.value)
    print(f"Symbols: {symbols}")
    # Create message
    message = create_message(symbols, Repitition.value)
    print(f"Message: {message}")
    # Simulate symbol errors based on the specified probability
    error_probability = SymbolErrorProbability.value
    if error_probability > 0:
        error_mask = np.random.rand(len(message)) < error_probability
        message[error_mask] = 1 - message[error_mask]
    print(f"Message after error simulation: {message}")
    # Decode message
    decoded_symbols = decode_message(message, Repitition.value)
    print(f"Decoded Symbols: {decoded_symbols}")
    # Demodulation
    decoded_bits = digital_demodulation(decoded_symbols, Constellation.value)
    print(f"Decoded Bits: {decoded_bits}")
    # Recovery
    recovered_bits = Recovery.value[1](decoded_bits)
    print(f"Recovered Bits: {recovered_bits}")
    # Compression
    decompressed_bits = Compression.value[1](recovered_bits, compression_data)
    print(f"Decompressed Bits: {decompressed_bits}")
    # Check if the original bitstring matches the decompressed bits
    if bitstring == decompressed_bits:
        print("Simulation successful: Original and decompressed bits match.")



sys.set_int_max_str_digits(0)  # Disable the limit on the number of digits in an integer
simulate(Compression.HUFFMAN, Recovery.REPETITION, Constellation.QAM8, SymbolErrorProbability.P0, Repitition.R1, "./files/text.txt")
    
