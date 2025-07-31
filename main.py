from simulations.simulation_local import simulate_local
from simulations.simulation_SDR import simulate_SDR

import sys
import time

from utils.enums.enums import Compression, Recovery, Constellation, Repitition
import csv
import os
import matplotlib.pyplot as plt
import itertools
import matplotlib.cm as cm

sys.set_int_max_str_digits(0) # Disable the limit on the number of digits in an integer

files = ["./files/text.txt", "./files/small_image.jpg", "./files/webpage.html"]

# Dictionary to store results for each file
file_results = {}

for filepath in files:
    file_results[filepath] = []
    
    for compression in Compression:
        for recovery in Recovery:
            for constellation in Constellation:
                for repetition in Repitition:
                    print(f"Running simulation for {compression.name}, {recovery.name}, {constellation.name}, {repetition.name} on {filepath}")
                    results = []
                    times = []
                    
                    for i in range(20):
                        print(f"Trial {i+1} Start")
                        start_time = time.time()
                        try:
                            diff = simulate_SDR(compression, recovery, constellation, repetition, filepath, 985e6)
                        except Exception as e:
                            print(f"Error during simulation: {e}")
                            continue  # Skip to the next trial if an error occurs
                        # exit()
                        end_time = time.time()
                        execution_time = end_time - start_time
                        print(f"Trial {i+1} - Difference: {diff}, Execution Time: {execution_time}")
                        if diff >=0 and execution_time >= 0:
                            results.append(diff)
                            times.append(execution_time)

                    # Calculate averages
                    avg_diff = -1
                    if len(results) != 0:
                        avg_diff = sum(results) / len(results)
                    avg_time = -1
                    if len(times) != 0:
                        avg_time = sum(times) / len(times)
                    
                    # Store result for this combination
                    file_results[filepath].append({
                        'combination': f"{compression.name}_{recovery.name}_{constellation.name}_{repetition.name}",
                        'avg_diff': avg_diff,
                        'avg_time': avg_time
                    })

# Use a repeating cycle of markers
markers = itertools.cycle(('o', 's', 'v', '^', '<', '>', 'd', 'P', '*', 'X', 'h'))

for filepath in files:
    plt.figure(figsize=(14, 10))

    x_values = [result['avg_time'] for result in file_results[filepath]]
    y_values = [result['avg_diff'] for result in file_results[filepath]]
    labels = [result['combination'] for result in file_results[filepath]]

    # Use colormap with enough distinct colors
    cmap = cm.get_cmap('tab20', len(labels))

    for i in range(len(labels)):
        color = cmap(i % cmap.N)
        marker = next(markers)
        plt.scatter(x_values[i], y_values[i], color=color, label=labels[i], marker=marker, s=50)

    plt.xlabel('Average Execution Time (seconds)')
    plt.ylabel('Average Bits in Error')
    plt.title(f'Performance Analysis for {os.path.basename(filepath)}')

    # Place legend outside plot
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize='x-small', ncol=1)
    plt.tight_layout()

    filename = f"./recieved_files/{os.path.basename(filepath)}_performance.png"
    plt.savefig(filename, bbox_inches='tight')  # Ensure legend is not cut off
    plt.close()
    
    # Save results to CSV for each file
    csv_filename = f"./recieved_files/{os.path.basename(filepath)}_performance.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Combination', 'Average_Time', 'Average_Bits_In_Error'])
        for result in file_results[filepath]:
            writer.writerow([result['combination'], result['avg_time'], result['avg_diff']])
