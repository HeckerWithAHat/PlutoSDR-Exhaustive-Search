import numpy as np
from PIL import Image

def int_to_bits(value, bit_length=16):
    return np.unpackbits(np.array([value], dtype=f'>u{bit_length // 8}').view(np.uint8))

def bits_to_int(bits):
    byte_array = np.packbits(bits)
    return int.from_bytes(byte_array, byteorder='big')

def image_to_bits(image_path, max_bits=20000):
    img = Image.open(image_path).convert('L')
    print(f"Original image size: {img.size}")
    img_array = np.asarray(img, dtype=np.uint8)
    flat_pixels = img_array.flatten()
    bitstream = np.unpackbits(flat_pixels)
    if len(bitstream) > max_bits:
        scale_factor = np.sqrt(max_bits / len(bitstream))
        new_w = int(img.size[0] * scale_factor)
        new_h = int(img.size[1] * scale_factor)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        print(f"Resized to {img.size}")
        img_array = np.asarray(img, dtype=np.uint8)
        flat_pixels = img_array.flatten()
        bitstream = np.unpackbits(flat_pixels)
    return bitstream, img.size

def bits_to_signal(bitstream, img_size, max_bits=20000):
    signal_data = 2 * bitstream.astype(np.float32) - 1
    
    # img info
    width_bits = int_to_bits(img_size[0], 16)
    height_bits = int_to_bits(img_size[1], 16)
    imginfo = np.concatenate([width_bits, height_bits])
    
    infoSignal = 2 * imginfo.astype(np.float32) - 1 
    transmit_signal = np.concatenate([infoSignal, signal_data])
    
    return transmit_signal.astype(np.complex64)

def signal_to_bits(signal, image_size=None, max_bits=20000):
    first32 = np.real(signal[:32])
    infobits = (first32 > 0).astype(int)
    
    width_bits = infobits[:16]
    height_bits = infobits[16:32]
    
    detected_width = bits_to_int(width_bits)
    detected_height = bits_to_int(height_bits)
    
    print(str(detected_width))
    print(str(detected_height))

    image_size = (detected_width, detected_height)
    
    expected_bits = 8 * image_size[0] * image_size[1]
    
    data_signal = signal[32:]
    
    bits = (np.real(data_signal[:expected_bits]) > 0).astype(np.uint8)
    
    return bits

def bits_to_image(bits, image_size):
    if len(bits) % 8 != 0:
        bits = np.pad(bits, (0, 8 - (len(bits) % 8)), constant_values=0)
    byte_data = np.packbits(bits)
    expected_bytes = image_size[0] * image_size[1]
    if len(byte_data) < expected_bytes:
        byte_data = np.pad(byte_data, (0, expected_bytes - len(byte_data)), constant_values=0)
        print(f"Padded byte data from {len(byte_data)} to {expected_bytes}")
    elif len(byte_data) > expected_bytes:
        byte_data = byte_data[:expected_bytes]
        print(f"Trimmed byte data to {expected_bytes}")
    try:
        img_array = byte_data.reshape((image_size[1], image_size[0]))
    except Exception as e:
        print(f"Reshape error: {e}")
        side = int(np.sqrt(len(byte_data)))
        img_array = byte_data[:side*side].reshape((side, side))
        print(f"Fallback reshape to {side}x{side}")
    return Image.fromarray(img_array, mode='L')