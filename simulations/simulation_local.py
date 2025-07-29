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
    
