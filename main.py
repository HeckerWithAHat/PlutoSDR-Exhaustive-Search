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

from utils.file_to_bitstring import file_to_bitstring

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
    bitstring = file_to_bitstring(filepath)

    



sys.set_int_max_str_digits(0)  # Disable the limit on the number of digits in an integer
simulate(Compression.HUFFMAN, Recovery.REPETITION, Constellation.QAM8, SymbolErrorProbability.P0, Repitition.R1, "./files/text.txt")
    
