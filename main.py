from simulations.simulation_local import simulate_local
from simulations.simulation_SDR import simulate_SDR

import sys
import time

from utils.enums.enums import Compression, Recovery, Constellation, Repitition
import csv
import os
import matplotlib.pyplot as plt

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
                    
                    for i in range(1):
                        print(f"Trial {i+1} Start")
                        start_time = time.time()
                        diff = simulate_SDR(compression, recovery, constellation, repetition, filepath, 985e6)
                        end_time = time.time()
                        execution_time = end_time - start_time
                        print(f"Trial {i+1} - Difference: {diff}, Execution Time: {execution_time}")
                        results.append(diff)
                        times.append(execution_time)
                    
                    # Calculate averages
                    avg_diff = sum(results) / len(results)
                    avg_time = sum(times) / len(times)
                    
                    # Store result for this combination
                    file_results[filepath].append({
                        'combination': f"{compression.name}_{recovery.name}_{constellation.name}_{repetition.name}",
                        'avg_diff': avg_diff,
                        'avg_time': avg_time
                    })

# Create one scatter plot for each file
for filepath in files:
    plt.figure(figsize=(12, 8))
    
    x_values = [result['avg_time'] for result in file_results[filepath]]
    y_values = [result['avg_diff'] for result in file_results[filepath]]
    labels = [result['combination'] for result in file_results[filepath]]
    
    plt.scatter(x_values, y_values)
    plt.xlabel('Average Execution Time (seconds)')
    plt.ylabel('Average Bits in Error')
    plt.title(f'Performance Analysis for {os.path.basename(filepath)}')
    
    # Optional: Add labels to points (might be crowded)
    # for i, label in enumerate(labels):
    #     plt.annotate(label, (x_values[i], y_values[i]), fontsize=8)
    
    filename = f"./recieved_files/{os.path.basename(filepath)}_performance.png"
    plt.savefig(filename)
    plt.close()
    
    # Save results to CSV for each file
    csv_filename = f"./recieved_files/{os.path.basename(filepath)}_performance.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Combination', 'Average_Time', 'Average_Bits_In_Error'])
        for result in file_results[filepath]:
            writer.writerow([result['combination'], result['avg_time'], result['avg_diff']])
