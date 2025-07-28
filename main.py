from utils.recovery.hamming import create_hamming_code_matrices
from utils.recovery.hamming import hamming_decode

from utils.compression.huffman import huffman_encoding
from utils.compression.huffman import huffman_decoding

from utils.compression.lempelziv import lempel_ziv_encoding
from utils.compression.lempelziv import lempel_ziv_decoding

from utils.recovery.reedsolomon import create_reed_solomon_generator_matrix
from utils.recovery.reedsolomon import decode_rs_erasure

from utils.recovery.repitition import repetition_encode
from utils.recovery.repitition import repetition_decode

from enum import Enum

class Compression(Enum):
    HUFFMAN = (huffman_encoding, huffman_decoding)
    LEMPEL_ZIV = (lempel_ziv_encoding, lempel_ziv_decoding)

class Recovery(Enum):
    HAMMING = (create_hamming_code_matrices, hamming_decode)
    REED_SOLOMON = (create_reed_solomon_generator_matrix, decode_rs_erasure)
    REPETITION = (repetition_encode, repetition_decode)

class Constellation(Enum):
    QAM2 = 2
    QAM4 = 4
    QAM8 = 8
    QAM16 = 16


class SymbolErrorProbability(Enum):
    P0 = 0.0
    P1 = 0.001
    P2 = 0.0001
    P3 = 0.00001
    P4 = 0.000001

class Repitition(Enum):
    R1 = 2
    R2 = 4
    R3 = 8
    R4 = 16
