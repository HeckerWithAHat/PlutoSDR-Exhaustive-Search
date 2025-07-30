from simulations.simulation_local import simulate_local
from simulations.simulation_SDR import simulate_SDR

import sys

from utils.enums.enums import Compression, Recovery, Constellation, Repitition
import csv
import os

sys.set_int_max_str_digits(0) # Disable the limit on the number of digits in an integer

# diff = simulate_SDR(Compression.HUFFMAN, Recovery.HAMMING, Constellation.QAM8, Repitition.R2, "./files/text.txt")
# print(diff)

files = ["./files/image.jpg", "./files/text.txt", "./files/audio.mp3", "./files/video.gif"]

for compression in Compression:
    for recovery in Recovery:
        for constellation in Constellation:
            for repetition in Repitition:
                for filepath in files:
                    print(f"Running simulation for {compression.name}, {recovery.name}, {constellation.name}, {repetition.name} on {filepath}")
                    results = []
                    for i in range(100):
                        print(f"Trial {i+1}")
                        diff = simulate_SDR(compression, recovery, constellation, repetition, filepath, 985e6)
                        results.append(diff)
                    import matplotlib.pyplot as plt

                    # Create filename base
                    filename_base = f"{compression.name}_{recovery.name}_{constellation.name}_{repetition.name}_{os.path.basename(filepath)}"

                    # Create scatter plot
                    plt.figure(figsize=(10, 6))
                    plt.scatter(range(len(results)), results)
                    plt.xlabel('Trial Number')
                    plt.ylabel('Difference')
                    plt.title(f'Results for {compression.name}_{recovery.name}_{constellation.name}_{repetition.name}')
                    plt.savefig(f"{filename_base}.png")
                    plt.close()

                    # Save results to CSV
                    with open(f"{filename_base}.csv", 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['Trial', 'Difference'])
                        for i, result in enumerate(results):
                            writer.writerow([i, result])
