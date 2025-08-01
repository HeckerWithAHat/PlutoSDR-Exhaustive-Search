import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import itertools
import os
import math
import warnings



markers = itertools.cycle(('o', 's', 'v', '^', '<', '>', 'd', 'P', '*', 'X', 'h'))

warnings.filterwarnings("ignore", category=DeprecationWarning)

def closest_to_origin(csv_path):
    closest_row = None
    min_distance = float('inf')

    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                time = float(row['Average_Time'])
                error = float(row['Average_Bits_In_Error'])

                if time < 0 or error < 0:
                    continue

                distance = math.sqrt(time ** 2 + error ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_row = {
                        'Combination': row['Combination'],
                        'Average_Time': time,
                        'Average_Bits_In_Error': error,
                        'Distance': distance
                    }
            except ValueError:
                continue 

    return closest_row


def create_scatter_plot(csv_file_path, graph_title):
    """
    Creates a scatter plot from CSV data with average execution time on x-axis 
    and log-scaled average bits in error on y-axis.
    
    Args:
        csv_file_path (str): Path to the CSV file
        graph_title (str): Title for the graph
    """
    print("Closest to (0,0):", closest_to_origin(csv_file_path)['Combination'])


    print(f"Creating scatter plot for {csv_file_path}...")
    # Read the CSV file
    with open(csv_file_path, 'r') as csvfile:
        file_results = csv.reader(csvfile)


        plt.figure(figsize=(14, 10))
        file_results = list(file_results)[1:]  # Skip header row

        x_values = [float(result[1]) if float(result[1]) != -1 else None for result in file_results]
        y_values = [float(result[2]) if float(result[2]) != -1 else None for result in file_results]
        labels = [result[0] for result in file_results]


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
        plt.show(block=False)




print("======")
print("IMAGE")
print("======")
create_scatter_plot('./recieved_files/small_image.jpg_performance.csv', 'Performance Analysis of A JPG Image Zoomed In')
print("======")
print("TEXT")
print("======")
create_scatter_plot('./recieved_files/text.txt_performance.csv', 'Performance Analysis of A Text File Zoomed In')
print("======")
print("HTML")
print("======")
create_scatter_plot('./recieved_files/webpage.html_performance.csv', 'Performance Analysis of A HTML File Zoomed In')
input("Press Enter to exit...")