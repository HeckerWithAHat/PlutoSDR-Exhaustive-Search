from utils.transmission.digital_modulation import digital_modulation
from utils.transmission.digital_modulation import digital_demodulation

from utils.file_to_bitstring import file_to_bitstring, bitstring_to_file

import numpy as np

from utils.enums.enums import Compression, Recovery, Constellation, Repitition

def simulate_SDR(Compression: Compression, Recovery: Recovery, Constellation: Constellation, Repitition: Repitition, filepath: str):
    """
    Simulates the compression and recovery process with the given parameters.
    
    Parameters:
        Compression - Enum value for compression method
        Recovery - Enum value for recovery method
        Constellation - Enum value for constellation size
        Repitition - Samples per signal
        filepath - Name of the file to save results
    """


    bitstring = file_to_bitstring(filepath)
    print("Original Bitstring:", bitstring)
    compressed_bitstring = Compression.value[0](bitstring[0])
    print("Compressed Bitstring:", compressed_bitstring)
    recovery_added_bitstring = Recovery.value[0](compressed_bitstring[0])
    print("Recovery Added Bitstring:", recovery_added_bitstring)
    modulated_signal = digital_modulation(recovery_added_bitstring[0], Constellation.value)
    import numpy as np
    message = np.array(modulated_signal[0])
    print("Final Message:", message)


    # -----------------------------------------------------
    # Imports
    # -----------------------------------------------------
    import matplotlib.pyplot as plt
    
    from PIL import Image
    from pathlib import Path
    import numpy as np
    import matplotlib.pyplot as plt
    import cv2
    from pathlib import Path

    from comms_lib.pluto import Pluto
    from comms_lib.system import DigitalCommSystem
    # ---------------------------------------------------------------
    # Digital communication system parameters.
    # ---------------------------------------------------------------
    fs = 10e6  # baseband sampling rate (samples per second)
    ts = 1 / fs  # baseband sampling period (seconds per sample)
    sps = Repitition.value  # samples per symbol (integer)
    T = ts * sps  # time between data symbols (seconds per symbol)

    # ---------------------------------------------------------------
    # Initialize transmitter and receiver.
    # ---------------------------------------------------------------
    tx = Pluto("ip:192.168.2.1")  # change to your Pluto device
    tx.tx_gain = 90  # set the transmitter gain

    rx = tx
    # # Uncomment the line below to use different Pluto devices for tx and rx
    # rx = Pluto("usb:7.6.5")
    # rx.rx_gain = 90  # set the receiver gain
    # ---------------------------------------------------------------
    # Initialize digital communication system and define system parameters.
    # ---------------------------------------------------------------
    system = DigitalCommSystem()
    system.set_transmitter(tx)
    system.set_receiver(rx)
    # tx.carrier_frequency = 984e6
    # rx.carrier_frequency = 984e6
    # ---------------------------------------------------------------
    # Initialize digital communication system and define system parameters.
    # ---------------------------------------------------------------
    system = DigitalCommSystem()
    system.set_transmitter(tx)
    system.set_receiver(rx)
    tx.carrier_frequency = 985e6
    rx.carrier_frequency = 985e6
    # transmit from Pluto!
    system.transmit_signal(
        message
    )  # keep transmit signal below 10,000 samples if possible, roughly around +/-1

    # receive from Pluto!
    receive_signal = system.receive_signal().tolist()
    print("Received Signal:", receive_signal)


    demodulated_signal = digital_demodulation(receive_signal, Constellation.value)
    print("Demodulated Signal:", demodulated_signal)
    uncovered_bitstring = Recovery.value[1](demodulated_signal, recovery_added_bitstring[1], recovery_added_bitstring[2])
    print("Uncovered Bitstring:", uncovered_bitstring)
    decompressed_bitstring = Compression.value[1](uncovered_bitstring, compressed_bitstring[1])
    
    print("Decompressed Bitstring:", decompressed_bitstring)
    bitstring_to_file(decompressed_bitstring, "decompressed_output.bin")


