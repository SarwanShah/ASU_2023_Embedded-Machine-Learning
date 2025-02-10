# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 20:02:27 2024

@author: sarwa
"""

def calculate_average_samples_per_second(file_path):
    total_samples = 0
    total_time = 0
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        prev_time = None
        
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue
            
            try:
                current_time = int(parts[0])
                total_samples += 1
                if prev_time is not None:
                    time_diff = current_time - prev_time
                    total_time += time_diff
                prev_time = current_time
            except ValueError:
                continue
    
    if total_samples > 0 and total_time > 0:
        average_samples_per_second = total_samples / (total_time / 1000)
        return average_samples_per_second
    else:
        return 0

# Example usage
file_path = "North.txt"  # Replace with the path to your text file
average_samples_per_second = calculate_average_samples_per_second(file_path)
print("Average Samples Per Second:", average_samples_per_second)
