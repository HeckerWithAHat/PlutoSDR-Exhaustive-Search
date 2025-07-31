import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import itertools
import os
import math

from yaml import warnings

markers = itertools.cycle(('o', 's', 'v', '^', '<', '>', 'd', 'P', '*', 'X', 'h'))


def create_scatter_plot(csv_file_path, graph_title):
    """
    Creates a scatter plot from CSV data with average execution time on x-axis 
    and log-scaled average bits in error on y-axis.
    
    Args:
        csv_file_path (str): Path to the CSV file
        graph_title (str): Title for the graph
    """
    # Read the CSV file
    with open(csv_file_path, 'r') as csvfile:
        file_results = csv.reader(csvfile)


        plt.figure(figsize=(14, 10))
        file_results = list(file_results)[1:]  # Skip header row

        x_values = [float(result[1]) if float(result[1]) != -1 else None for result in file_results]
        y_values = [float(result[2]) if float(result[2]) != -1 else None for result in file_results]
        labels = [result[0] for result in file_results]

        smallest_method_index = 0

        for i in range(1, len(labels)):
            if y_values[i] is None or x_values[i] is None:
                continue
            best_distance = math.sqrt(x_values[i]**2 + y_values[i]**2)
            if best_distance > math.sqrt(x_values[smallest_method_index]**2 + y_values[smallest_method_index]**2):
                smallest_method_index = i

        print(f"Best method: {labels[smallest_method_index]} with distance {math.sqrt(x_values[smallest_method_index]**2 + y_values[smallest_method_index]**2)}")
        # warnings.filterwarnings("ignore", category=DeprecationWarning)
        # Use colormap with enough distinct colors
        cmap = cm.get_cmap('tab20', len(labels))

        for i in range(len(labels)):
            color = cmap(i % cmap.N)
            marker = next(markers)
            plt.scatter(x_values[i], y_values[i], color=color, label=labels[i], marker=marker, s=50)

        plt.xlabel('Average Execution Time (seconds)')
        plt.ylabel('Average Bits in Error')
        plt.title(graph_title)
        # plt.yscale('log')
       


        # Place legend outside plot
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize='x-small', ncol=2)
        plt.tight_layout()
        plt.show()

create_scatter_plot('./recieved_files/small_image.jpg_performance.csv', 'Performance Analysis of A JPG Image')