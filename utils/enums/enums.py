from utils.recovery.hamming import encode_bitstring_hamming
from utils.recovery.hamming import hamming_decode

from utils.compression.huffman import huffman_encoding
from utils.compression.huffman import huffman_decoding

from utils.compression.lempelziv import lempel_ziv_encoding
from utils.compression.lempelziv import lempel_ziv_decoding

from utils.recovery.reedsolomon import reed_solomon_encode
from utils.recovery.reedsolomon import reed_solomon_decode

from utils.recovery.repitition import repetition_encode
from utils.recovery.repitition import repetition_decode

from utils.transmission.digital_modulation import digital_modulation
from utils.transmission.digital_modulation import digital_demodulation

from utils.transmission.create_message import create_message
from utils.transmission.create_message import decode_message

from utils.file_to_bitstring import file_to_bitstring

from enum import Enum

class Compression(Enum):
    HUFFMAN = (huffman_encoding, huffman_decoding)
    LEMPEL_ZIV = (lempel_ziv_encoding, lempel_ziv_decoding)

class Recovery(Enum):
    HAMMING = (encode_bitstring_hamming, hamming_decode)
    REED_SOLOMON = (reed_solomon_encode, reed_solomon_decode)
    REPETITION = (repetition_encode, repetition_decode)

class Constellation(Enum):
    QAM2 = 2
    QAM4 = 4
    QAM8 = 8
    QAM16 = 16



class Repitition(Enum):
    R1 = 2
    R2 = 4
    R3 = 6
    R4 = 8

