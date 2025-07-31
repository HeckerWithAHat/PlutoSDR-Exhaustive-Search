import csv
import math

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

if __name__ == "__main__":
    print("======")
    print("IMAGE")
    print("======")
    path = './files/small_image.jpg_performance.csv' 
    result = closest_to_origin(path)
    if result:
        print("Closest to (0,0):")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("No valid data found.")

    print("======")
    print("TEXT")
    print("======")
    path = './files/text.txt_performance.csv'
    result = closest_to_origin(path)
    if result:
        print("Closest to (0,0):")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("No valid data found.")
    
    print("======")
    print("HTML")
    print("======")
    path = './files/webpage.html_performance.csv'
    result = closest_to_origin(path)
    if result:
        print("Closest to (0,0):")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("No valid data found.")