from simulations.simulation_local import simulate_local
from simulations.simulation_SDR import simulate_SDR

import sys

from utils.enums.enums import Compression, Recovery, Constellation, Repitition

sys.set_int_max_str_digits(0) # Disable the limit on the number of digits in an integer

simulate_SDR(Compression.HUFFMAN, Recovery.HAMMING, Constellation.QAM8, Repitition.R2, "./files/text.txt", carrier_frequency = 984e6)