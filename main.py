from simulations.simulation_local import simulate_local
from simulations.simulation_SDR import simulate_SDR

import sys

from utils.enums.enums import Compression, Recovery, Constellation, Repitition
import csv
import os
import time

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
                    times = []
                    for i in range(100):
                        print(f"Trial {i+1}")
                        start_time = time.time()
                        diff = simulate_SDR(compression, recovery, constellation, repetition, filepath, 985e6)
                        end_time = time.time()
                        duration = end_time - start_time

                        times.append(duration)
                        results.append(diff)


                    import matplotlib.pyplot as plt

                    # Create filename base
                    filename_base = f"{compression.name}_{recovery.name}_{constellation.name}_{repetition.name}_{os.path.basename(filepath)}"

                    # Create scatter plot
                    import matplotlib.pyplot as plt
                    total_time = sum(times)

                    # Dual-axis plot
                    fig, ax1 = plt.subplots(figsize=(10, 6))

                    # Plot Difference (left y-axis)
                    ax1.set_xlabel('Trial Number')
                    ax1.set_ylabel('Difference', color='tab:blue')
                    ax1.scatter(range(len(results)), results, color='tab:blue', label='Difference', alpha=0.7)
                    ax1.tick_params(axis='y', labelcolor='tab:blue')

                    # Plot Time on second y-axis
                    ax2 = ax1.twinx()
                    ax2.set_ylabel('Time (s)', color='tab:orange')
                    ax2.plot(range(len(times)), times, color='tab:orange', label='Time per Trial', linewidth=2)
                    ax2.tick_params(axis='y', labelcolor='tab:orange')

                    # Title with total time
                    plt.title(f'{compression.name}_{recovery.name}_{constellation.name}_{repetition.name}\nTotal Time: {total_time:.2f} s')

                    # Add legends from both axes
                    lines_1, labels_1 = ax1.get_legend_handles_labels()
                    lines_2, labels_2 = ax2.get_legend_handles_labels()
                    plt.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

                    # Save and close
                    plt.tight_layout()
                    plt.savefig(f"{filename_base}.png")
                    plt.close()


                    # Save results to CSV
                    with open(f"{filename_base}.csv", 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['Trial', 'Difference', 'Time (s)'])
                        for i, (result, duration) in enumerate(zip(results, times)):
                            writer.writerow([i, result, duration])