# # %%
# # ruff: noqa: F405
# import os
# from pathlib import Path

# import matplotlib.pyplot as plt
# import numpy as np
# from IPython import get_ipython
# from PIL import Image

# from comms_lib.dsp import (
#     get_qam_constellation,
#     qam_mapper,
# )

# # from comms_lib.qam import qam_modulator as qam_mapper
# # from comms_lib.qam import qam_demodulator as qam_demapper
# from comms_lib.pluto import Pluto
# from comms_lib.system3 import DigitalTransmitter, SystemConfiguration

# if get_ipython() is not None:
#     get_ipython().run_line_magic("reload_ext", "autoreload")
#     get_ipython().run_line_magic("autoreload", "2")

# os.chdir(Path(__file__).parent)

# # ---------------------------------------------------------------
# # Digital communication system parameters.
# # ---------------------------------------------------------------
# fs = 5e6  # baseband sampling rate (samples per second)
# sps = 1

# # ---------------------------------------------------------------
# # Create shared system configuration
# # ---------------------------------------------------------------
# modulation_order = 16  # 4, 16, 64, 256, etc.
# # Size of the image to transmit, need to be the same for both TX and RX
# IMAGE_SIZE = (32, 32)

# config = SystemConfiguration(
#     modulation_order=modulation_order,
#     n_pilot_syms=1500,
#     seed=123456,
#     carrier_frequency = 985e6,
#     rx_gain=100
# )
# config.sample_rate = fs
# config.sps = 10

# config.save_to_file(Path(__file__).parent / "system_config.json")

# # ---------------------------------------------------------------
# # Initialize separate transmitter and receiver with SDR devices
# # ---------------------------------------------------------------
# tx_sdr = Pluto("ip:192.168.2.1")  # change to your Pluto device
# # Create transmitter and receiver with shared configuration
# tx = DigitalTransmitter(config, tx_sdr)
# # Set gains
# tx.set_gain(100)
# # transmitter.sdr.tx_hardwaregain_chan0 = 0

# # ---------------------------------------------------------------
# # Prepare data to transmit
# # ---------------------------------------------------------------
# # Digital modulation parameters

# constellation = get_qam_constellation(modulation_order, Es=1)

# # Load and prepare image
# img = Image.open(Path(__file__).parent / "tower.png")
# img = img.resize(IMAGE_SIZE)
# img = np.array(img)
# # print(img)
# bits = np.unpackbits(img)
# # print(bits)

# # Map bits to symbols
# tx_syms, padding = qam_mapper(bits, constellation)
# num_transmit_symbols = len(tx_syms)
# print("Number of transmit symbols: ", num_transmit_symbols)

# # Shuffle symbols if desired
# # shuffler = np.random.default_rng().permutation(num_transmit_symbols)
# # transmit_symbols_shuffled = transmit_symbols[shuffler]

# tx_syms_shuffled = tx_syms
# print(tx_syms_shuffled)

# # ---------------------------------------------------------------
# # Transmit and receive
# # ---------------------------------------------------------------
# # Transmit signal (let the transmitter handle pulse shaping internally)
# print("Transmitting signal...")
# tx.transmit_signal(tx_syms_shuffled)




from utils.enums.enums import Compression, Recovery, Constellation, Repitition
from utils.transmission.digital_modulation import digital_modulation, digital_demodulation
from utils.file_to_bitstring import file_to_bitstring, bitstring_to_file


def transmit_image(filepath:str):
    bitstring = file_to_bitstring(filepath)
    # print("Original Bitstring:", bitstring)
    compressed_bitstring = Compression.LEMPEL_ZIV.value[0](bitstring[0])
    # print("Compressed Bitstring:", compressed_bitstring)
    recovery_added_bitstring = Recovery.REPETITION.value[0](compressed_bitstring[0])
    # print("Recovery Added Bitstring:", recovery_added_bitstring)
    modulated_signal = digital_modulation(recovery_added_bitstring[0], Constellation.PAM4.value)
    import numpy as np
    message = np.array(modulated_signal[0])

    import matplotlib.pyplot as plt
    import numpy as np
    from IPython import get_ipython
    from PIL import Image
    from comms_lib.pluto import Pluto
    from comms_lib.system3 import DigitalTransmitter, SystemConfiguration
    import os
    from pathlib import Path


    if get_ipython() is not None:
        get_ipython().run_line_magic("reload_ext", "autoreload")
        get_ipython().run_line_magic("autoreload", "2")

    os.chdir(Path(__file__).parent)

    # ---------------------------------------------------------------
    # Digital communication system parameters.
    # ---------------------------------------------------------------
    fs = 5e6  # baseband sampling rate (samples per second)
    sps = Repitition.R2.value  # samples per symbol (integer)
    modulation_order = Constellation.PAM4.value  # 4, 16, 64, 256, etc.
    # ---------------------------------------------------------------
    config = SystemConfiguration(
        modulation_order=modulation_order,
        n_pilot_syms=1500,
        seed=123456,
        carrier_frequency = 985e6,
        rx_gain=100
    )
    config.sample_rate = fs
    config.sps = 10

    config.save_to_file(Path(__file__).parent / "system_config.json")

    # ---------------------------------------------------------------
    # Initialize separate transmitter and receiver with SDR devices
    # ---------------------------------------------------------------
    tx_sdr = Pluto("ip:192.168.2.1")  # change to your Pluto device
    # Create transmitter and receiver with shared configuration
    tx = DigitalTransmitter(config, tx_sdr)
    # Set gains
    tx.set_gain(100)
    tx.transmit_signal(message)

    # export configuration to for receiver
    tx.config.save_to_file(Path(__file__).parent / "tx_config.json")
    print("Transmitter configuration saved to tx_config.json")

    print("\nTransmitter configuration:")
    print(f"  Sample rate: {tx.config.sample_rate/1e6:.1f} MHz")
    print(f"  Samples per symbol: {tx.config.sps}")
    print(f"  Carrier frequency: {tx.config.carrier_frequency/1e6:.0f} MHz")
    print(f"  TX gain: {tx.config.tx_gain}")

import sys

sys.set_int_max_str_digits(0) # Disable the limit on the number of digits in an integer
transmit_image("./files/small_image.jpg")  # Replace with your image file path