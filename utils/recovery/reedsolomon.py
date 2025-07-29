from reedsolo import RSCodec

def bits_to_bytes(bitstring: str) -> bytes:
    padded = bitstring + '0' * ((8 - len(bitstring) % 8) % 8)
    return int(padded, 2).to_bytes(len(padded) // 8, byteorder='big')

def bytes_to_bits(byte_data: bytes) -> str:
    return ''.join(f'{byte:08b}' for byte in byte_data)

def reed_solomon_encode(bitstring: str, ecc_bytes: int = 10) -> bytes:
    """
    Encodes a bitstring using Reed-Solomon coding.
    
    Parameters:
        bitstring: String of bits (e.g., "110101")
        ecc_bytes: Number of ECC (error correction) bytes to add

    Returns:
        Encoded data as bytes (original data + ECC)
    """
    rsc = RSCodec(ecc_bytes)
    data_bytes = bits_to_bytes(bitstring)
    encoded = rsc.encode(data_bytes)
    return encoded

def reed_solomon_decode(encoded_data: bytes, ecc_bytes: int = 10) -> str:
    """
    Decodes a Reed-Solomon encoded message.

    Parameters:
        encoded_data: Bytes from reed_solomon_encode
        ecc_bytes: Number of ECC bytes used in encoding

    Returns:
        Original bitstring as a string of '0' and '1'
    """
    rsc = RSCodec(ecc_bytes)
    decoded = rsc.decode(encoded_data)[0]  # Returns (data, ecc)
    return bytes_to_bits(decoded)




# original_bits = "1101001110110010"
# encoded = reed_solomon_encode(original_bits, ecc_bytes=10)

# # Introduce an error
# corrupted = bytearray(encoded)
# corrupted[2] ^= 0b00010000  # flip a bit in the 3rd byte

# decoded_bits = reed_solomon_decode(corrupted, ecc_bytes=10)
# print("Original bits: ", original_bits)
# print("Decoded bits : ", decoded_bits[:len(original_bits)])
