from simulations.simulation_local import simulate_local
import sys

from utils.enums.enums import Compression, Recovery, Constellation, SymbolErrorProbability, Repitition

sys.set_int_max_str_digits(0) # Disable the limit on the number of digits in an integer

simulate_local(Compression.HUFFMAN, Recovery.REPETITION, Constellation.QAM8, SymbolErrorProbability.P0, Repitition.R1, "./files/text.txt")