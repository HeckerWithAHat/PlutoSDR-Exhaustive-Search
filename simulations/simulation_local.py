from utils.transmission.digital_modulation import digital_modulation
from utils.transmission.digital_modulation import digital_demodulation

from utils.transmission.create_message import create_message
from utils.transmission.create_message import decode_message

from utils.file_to_bitstring import file_to_bitstring

import numpy as np

from utils.enums.enums import Compression, Recovery, Constellation, SymbolErrorProbability, Repitition

def simulate_local(Compression: Compression, Recovery: Recovery, Constellation: Constellation, SymbolErrorProbability: SymbolErrorProbability, Repitition: Repitition, filepath: str):
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
    print("Original Bitstring:", bitstring)
    compressed_bitstring = Compression.value[0](bitstring[0])
    print("Compressed Bitstring:", compressed_bitstring)
    recovery_added_bitstring = Recovery.value[0](compressed_bitstring[0])
    print("Recovery Added Bitstring:", recovery_added_bitstring)
    modulated_signal = digital_modulation(recovery_added_bitstring, Constellation.value)
    print("Modulated Signal:", modulated_signal)
    message = create_message(modulated_signal[0], Repitition.value)
    print("Final Message:", message)
