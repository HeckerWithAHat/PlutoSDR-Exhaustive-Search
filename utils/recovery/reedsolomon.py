from reedsolo import RSCodec

def bits_to_bytes(bitstring: str) -> bytes:
    padded = bitstring + '0' * ((8 - len(bitstring) % 8) % 8)
    return int(padded, 2).to_bytes(len(padded) // 8, byteorder='big')

def bytes_to_bits(byte_data: bytes) -> str:
    return ''.join(f'{byte:08b}' for byte in byte_data)

def reed_solomon_encode(bitstring: str) -> bytes:
    """
    Encodes a bitstring using Reed-Solomon coding.
    
    Parameters:
        bitstring: String of bits (e.g., "110101")
        ecc_bytes: Number of ECC (error correction) bytes to add

    Returns:
        Encoded data as bytes (original data + ECC)
    """
    rsc = RSCodec(100)
    data_bytes = bits_to_bytes(bitstring)
    encoded = rsc.encode(data_bytes)
    return [bytes_to_bits(encoded), len(bitstring), 0]

def reed_solomon_decode(encoded_data: str, original_length: int, _) -> str:
    """
    Decodes a Reed-Solomon encoded message.

    Parameters:
        encoded_data: Bytes from reed_solomon_encode
        original_length: Original length of the bitstring

    Returns:
        Original bitstring as a string of '0' and '1', or None if decoding fails
    """
    try:
        encoded_data = bits_to_bytes(encoded_data)
        rsc = RSCodec(100)
        decoded = rsc.decode(encoded_data)[0]  # Returns (data, ecc)
        return bytes_to_bits(decoded)[:original_length]  # Return only the original length of bits
    except Exception as e:
        print(f"Reed-Solomon decoding failed: {e}")
        return None