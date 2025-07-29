from utils.transmission.digital_modulation import digital_modulation
from utils.transmission.digital_modulation import digital_demodulation

from utils.transmission.create_message import create_message
from utils.transmission.create_message import decode_message

from utils.file_to_bitstring import file_to_bitstring, bitstring_to_file

import numpy as np

from utils.enums.enums import Compression, Recovery, Constellation, SymbolErrorProbability, Repitition

def simulate_local(Compression: Compression, Recovery: Recovery, Constellation: Constellation, Repitition: Repitition, filepath: str):
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

    # import numpy as np
    # import matplotlib.pyplot as plt
    # from PIL import Image
    # from comms_lib.pluto import Pluto
    # from comms_lib.system import DigitalCommSystem

    # fs = 10e6  # baseband sampling rate (samples per second)
    # ts = 1 / fs  # baseband sampling period (seconds per sample)
    # sps = 3
    # T = ts * sps  # time between data symbols (seconds per symbol)

    # tx = Pluto("usb:2.6.5")  # change to your Pluto device
    # tx.tx_gain = 60  # set the transmitter gain

    # rx = tx
    # # Uncomment the line below to use different Pluto devices for tx and rx
    # # rx = Pluto("usb:7.6.5")
    # rx.rx_gain = 60 

    bitstring = file_to_bitstring(filepath)
    print("Original Bitstring:", bitstring)
    compressed_bitstring = Compression.value[0](bitstring[0])
    print("Compressed Bitstring:", compressed_bitstring)
    recovery_added_bitstring = Recovery.value[0](compressed_bitstring[0])
    print("Recovery Added Bitstring:", recovery_added_bitstring[0])
    print("H:", recovery_added_bitstring[1])
    print("Padding Count:", recovery_added_bitstring[2])
    modulated_signal = digital_modulation(recovery_added_bitstring, Constellation.value)
    print("Modulated Signal:", modulated_signal)
    message = create_message(modulated_signal[0], Repitition.value)
    print("Final Message:", message)

    decoded_message = decode_message(message, Repitition.value)
    print("Decoded Message:", decoded_message)
    demodulated_signal = digital_demodulation(decoded_message, Constellation.value)
    print("Demodulated Signal:", demodulated_signal)
    uncovered_bitstring = Recovery.value[1](demodulated_signal, recovery_added_bitstring[1], recovery_added_bitstring[2])
    print("Uncovered Bitstring:", uncovered_bitstring)
    decompressed_bitstring = Compression.value[1](uncovered_bitstring, compressed_bitstring[1])
    print("Decompressed Bitstring:", decompressed_bitstring)
    bitstring_to_file(decompressed_bitstring, "decompressed_output.bin")


    # system = DigitalCommSystem()
    # system.set_transmitter(tx)
    # system.set_receiver(rx)
    # tx.carrier_frequency = 950e6
    # rx.carrier_frequency = 950e6

    # system.transmit_signal(message.astype(np.complex64))

    # receive_signal = system.receive_signal()


    # # plot transmitted and received signals
    # plt.figure(figsize=(12, 10))
    # plt.subplot(2, 1, 1)
    # plt.plot(np.real(message), color="blue", marker="o", label="Real Transmit")
    # plt.plot(np.real(receive_signal), color="red", label="Real Receive")
    # plt.title("Transmit and Receive Signals (Real)")
    # plt.xlabel("Time Samples")
    # plt.ylabel("Amplitude")
    # plt.grid(True)
    # plt.legend()

    # plt.subplot(2, 1, 2)
    # plt.plot(np.imag(message), color="blue", marker="o", label="Imaginary Transmit")
    # plt.plot(np.imag(receive_signal), color="red", label="Imaginary Receive")
    # plt.title("Transmit and Receive Signals (Imaginary)")
    # plt.xlabel("Time Samples")
    # plt.ylabel("Amplitude")
    # plt.grid(True)
    # plt.legend()

    # plt.show()


    # receive_symbols = receive_signal[sps // 2 :: sps]

    # fig, ax = plt.subplots()
    # ax.scatter(np.real(receive_symbols), np.imag(receive_symbols), color='blue', label='Received Symbols')
    # ax.scatter(np.real(message), np.imag(message), color='red', label='Transmitted Symbols', alpha=0.5)
    # ax.set_title('Received Symbols in Constellation') 
    # ax.set_xlabel('In-Phase Component')
    # ax.set_ylabel('Quadrature Component')
    # plt.show()

    # print("Received Symbols:", receive_symbols)
