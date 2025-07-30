import numpy as np

def bits_to_signal(bitstream, img_size, max_bits=20000):
    signal_data = 2 * bitstream.astype(np.float32) - 1  # BPSK: 0 -> -1, 1 -> +1

    sync_pattern = [0.9, -0.9, 0.9, -0.9]
    width_norm = img_size[0] / 1000.0
    height_norm = img_size[1] / 1000.0
    length_norm = len(signal_data) / max_bits

    metadata = np.array([
        sync_pattern[0] + 1j * sync_pattern[1],
        sync_pattern[2] + 1j * sync_pattern[3],
        width_norm + 1j * height_norm,
        length_norm + 1j * 0,
        0 + 1j * 0, 0 + 1j * 0,
        0 + 1j * 0, 0 + 1j * 0,
        0 + 1j * 0, 0 + 1j * 0
    ], dtype=np.complex64)

    transmit_signal = np.concatenate([metadata, signal_data + 0j])
    return transmit_signal

def signal_to_bits(signal, image_size, max_bits=20000):
    data_start = 10
    data_signal = signal[data_start:]
    estimated_bits = 8 * image_size[0] * image_size[1]
    bits = (np.real(data_signal[:estimated_bits]) > 0).astype(np.uint8)
    return bits

def bytes_to_bits(data: bytes) -> np.ndarray:
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8))

def bits_to_bytes(bits: np.ndarray) -> bytes:
    if len(bits) % 8 != 0:
        bits = np.pad(bits, (0, 8 - len(bits) % 8), constant_values=0)
    byte_array = np.packbits(bits)
    return byte_array.tobytes()

def text_to_signal(text, max_bits=20000):
    byte_data = text.encode('utf-8')
    bitstream = bytes_to_bits(byte_data)
    bitstream = bitstream[:max_bits]
    return bits_to_signal(bitstream, (0, 0), max_bits), len(bitstream)

def signal_to_text(signal, bit_length, max_bits=20000):
    bits = (np.real(signal[10:10 + bit_length]) > 0).astype(np.uint8)
    byte_data = bits_to_bytes(bits)
    return byte_data.decode('utf-8', errors='ignore')
