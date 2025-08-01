# # %%
# # ruff: noqa: F405


# from comms_lib.dsp import (
#     calc_symbol_error_rate,
#     demod_nearest,
#     get_qam_constellation,
#     qam_demapper,
#     qam_mapper,
# )
# from comms_lib.pluto import Pluto
# from comms_lib.system3 import DigitalReceiver, SystemConfiguration

# if get_ipython() is not None:
#     get_ipython().run_line_magic("reload_ext", "autoreload")
#     get_ipython().run_line_magic("autoreload", "2")

# os.chdir(Path(__file__).parent)

# # ---------------------------------------------------------------
# # Digital communication system parameters.
# # ---------------------------------------------------------------
# fs = 5e6  # baseband sampling rate (samples per second)
# sps = 1
# # Size of the image to transmit, need to be the same for both TX and RX
# IMAGE_SIZE = (32, 32)

# # ---------------------------------------------------------------
# # Create shared system configuration
# # ---------------------------------------------------------------
# config = SystemConfiguration.from_file(Path(__file__).parent / "tx_config.json")
# modulation_order = config.modulation_order

# rx_sdr = Pluto("ip:192.168.2.1")  # Uncomment to use different device
# rx = DigitalReceiver(config, rx_sdr)
# rx.set_gain(100)

# # Set RF bandwidth
# # tx.tx_rf_bandwidth = rx.rx_rf_bandwidth = int(tx.sample_rate / config.sps) * 2

# # ---------------------------------------------------------------
# # Prepare data to transmit
# # ---------------------------------------------------------------
# # Digital modulation parameters

# constellation = get_qam_constellation(modulation_order, Es=1)

# # Load and prepare image
# img = Image.open(Path(__file__).parent / "tower.png")
# img = img.resize(IMAGE_SIZE)
# img = np.array(img)
# bits = np.unpackbits(img)

# # Map bits to symbols
# tx_syms, padding = qam_mapper(bits, constellation)
# num_transmit_symbols = len(tx_syms)
# print("Number of transmit symbols: ", num_transmit_symbols)

# # Shuffle symbols if desired
# # shuffler = np.random.default_rng().permutation(num_transmit_symbols)
# # transmit_symbols_shuffled = transmit_symbols[shuffler]

# tx_syms_shuffled = tx_syms


# # Receive signal
# print("Receiving signal...")
# receive_signal = rx.receive_signal()

# print("=" * 60)
# # ---------------------------------------------------------------
# # Process received signal
# # ---------------------------------------------------------------
# # The receiver already handles pulse shaping, timing sync, frequency sync, and channel equalization
# # So receive_signal contains the equalized symbols ready for demodulation
# rx_syms = receive_signal
# print("Number of receive symbols: ", len(rx_syms))

# # Associate received symbols with nearest in constellation
# det_rx_syms_shuffled = demod_nearest(rx_syms, constellation)

# # Unshuffle received symbols
# # detected_receive_symbols = detected_receive_symbols_shuffled[np.argsort(shuffler)]
# det_rx_syms = det_rx_syms_shuffled

# # Demap symbols to bits
# rx_bits = qam_demapper(det_rx_syms, padding, constellation)

# print("")

# # Calculate error rates
# ser = calc_symbol_error_rate(tx_syms, det_rx_syms)
# print("Symbol error rate: ", ser)

# ber = calc_symbol_error_rate(bits, rx_bits)
# print("Bit error rate: ", ber)

# # ---------------------------------------------------------------
# # Plotting
# # ---------------------------------------------------------------
# # Plot transmitted and received signals and symbols
# fig = plt.figure(figsize=(12, 6))

# # Top subplot for real symbols
# ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1)
# ax1.plot(
#     np.real(tx_syms_shuffled), color="blue", marker="o", label="Real Transmit Symbols"
# )
# ax1.plot(np.real(rx_syms), color="red", label="Real Receive Symbols")
# ax1.set_title("Transmit and Receive Symbols (Real)")
# ax1.set_xlabel("Symbol Index")
# ax1.set_ylabel("Amplitude")
# ax1.grid(True)
# ax1.legend()

# # Bottom subplot for imaginary symbols
# ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=1)
# ax2.plot(
#     np.imag(tx_syms_shuffled),
#     color="blue",
#     marker="o",
#     label="Imaginary Transmit Symbols",
# )
# ax2.plot(np.imag(rx_syms), color="red", label="Imaginary Receive Symbols")
# ax2.set_title("Transmit and Receive Symbols (Imaginary)")
# ax2.set_xlabel("Symbol Index")
# ax2.set_ylabel("Amplitude")
# ax2.grid(True)
# ax2.legend()

# # Right side square subplot for symbols
# ax3 = plt.subplot2grid((2, 2), (0, 1), rowspan=2, aspect="equal")
# ax3.scatter(
#     np.real(rx_syms),
#     np.imag(rx_syms),
#     color="red",
#     label="Received Symbols",
# )
# ax3.scatter(
#     np.real(tx_syms),
#     np.imag(tx_syms),
#     color="blue",
#     label="Transmitted Symbols",
# )
# ax3.set_title("Transmitted and Received Symbols")
# ax3.set_xlabel("Real Component")
# ax3.set_ylabel("Imaginary Component")
# ax3.grid(True)
# ax3.legend()
# plt.tight_layout()
# plt.show()

# # Plot the received image
# rx_img = np.packbits(rx_bits[: rx_bits.shape[0] - padding]).reshape(img.shape)
# fig, ax = plt.subplots(1, 2, figsize=(12, 6))
# ax[0].imshow(img)
# ax[0].set_title("Original Image")
# ax[0].axis("off")
# ax[1].imshow(rx_img)
# ax[1].set_title("Received Image")
# ax[1].axis("off")
# plt.tight_layout()
# plt.show()

# # ---------------------------------------------------------------
# # Demonstrate separate TX/RX usage
# # ---------------------------------------------------------------
# print("\n" + "=" * 60)
# print("DEMONSTRATING SEPARATE TX/RX OPERATION")
# print("=" * 60)

# # Example: Using transmitter and receiver independently


# print("\nReceiver configuration:")
# print(f"  Sample rate: {rx.config.sample_rate/1e6:.1f} MHz")
# print(f"  Samples per symbol: {rx.config.sps}")
# print(f"  Carrier frequency: {rx.config.carrier_frequency/1e6:.0f} MHz")
# print(f"  RX gain: {rx.config.rx_gain}")

# print("\nShared configuration ensures compatibility:")
# print(f"  Preamble length: {len(config.preamble_symbols)} symbols")
# print(f"  STF symbols: {config.num_stf_symbols}")
# print(f"  LTF symbols: {config.num_ltf_symbols}")
# print(f"  Pilot symbols: {config.n_pilot_syms}")

# %%



def recieve_image(filepath_to_save):
    
    import os
    from pathlib import Path

    import matplotlib.pyplot as plt
    import numpy as np
    from IPython import get_ipython
    from PIL import Image
    from comms_lib.pluto import Pluto
    from comms_lib.system3 import DigitalReceiver, SystemConfiguration
    from utils.enums.enums import Compression, Recovery, Constellation, Repitition
    from utils.transmission.digital_modulation import digital_modulation, digital_demodulation
    from utils.file_to_bitstring import file_to_bitstring, bitstring_to_file

    if get_ipython() is not None:
        get_ipython().run_line_magic("reload_ext", "autoreload")
        get_ipython().run_line_magic("autoreload", "2")

    os.chdir(Path(__file__).parent)

    # ---------------------------------------------------------------
    # Digital communication system parameters.
    # ---------------------------------------------------------------
    fs = 5e6  # baseband sampling rate (samples per second)
    sps = Repitition.R2.value


    config = SystemConfiguration.from_file(Path(__file__).parent / "tx_config.json")
    modulation_order = config.modulation_order

    rx_sdr = Pluto("ip:192.168.2.1")  # Uncomment to use different device
    rx = DigitalReceiver(config, rx_sdr)
    rx.set_gain(30)
    receive_signal = rx.receive_signal().tolist()
    print("Received Signal:", receive_signal)
    demodulated_signal = digital_demodulation(receive_signal, Constellation.PAM4.value)
    print("Demodulated Signal:", demodulated_signal)
    uncovered_bitstring = Recovery.REED_SOLOMON.value[1](demodulated_signal, 6624, 0)
    print("Uncovered Bitstring:", uncovered_bitstring)
    # decompressed_bitstring = Compression.HUFFMAN.value[1](uncovered_bitstring)
    print("Decompressed Bitstring:", uncovered_bitstring)
    bitstring_to_file(uncovered_bitstring, filepath_to_save)



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
    return [bitstream, img.size]

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







import sys


sys.set_int_max_str_digits(0) # Disable the limit on the number of digits in an integer

recieve_image("./recieved_files/received_text.txt")
