'''
# Initialize variables to store total matches count and total execution time
total_matches_count = 0
total_execution_time = 0
matches_instances = 0

# Read the file line by line
with open('men_have_strictly_ordered_lists/results/gsa1_model_size_1000.txt', 'r') as file:
    lines = file.readlines()

    # Loop through the lines
    for i in range(0, len(lines), 7):  # Assuming each instance takes 5 lines in the file
        # Extracting matches and execution time information
        matches_line = lines[i + 3]
        execution_time_line = lines[i + 1]

        # Extracting matches count
        matches_count = matches_line.count("'w")
        total_matches_count += matches_count

        # Extracting execution time (with error handling)
        split_line = execution_time_line.split()
        if len(split_line) >= 3:  # Check if there are enough elements to extract time
            try:
                execution_time = float(split_line[-2])
                total_execution_time += execution_time
                matches_instances += 1
            except ValueError:
                print(f"Skipping invalid execution time in line: {execution_time_line}")
        else:
            print(f"Skipping invalid format in line: {execution_time_line}")

# Calculate averages
average_matches = total_matches_count / matches_instances if matches_instances > 0 else 0
average_execution_time = total_execution_time / matches_instances if matches_instances > 0 else 0

# Print the averages
print(f"Average stable matching size: {average_matches}")
print(f"Average execution time: {average_execution_time} seconds")
'''
import os
from collections import defaultdict

folder_path = 'men_have_strictly_ordered_lists/results/'  # Replace this with the path to your folder

# Create a dictionary to store data by model and size
data = defaultdict(lambda: defaultdict(list))

# Iterate through files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.txt'):
        # Extract model, size, and type from the filename
        parts = filename.split('_')
        model = parts[0].capitalize()  # Get the model name (capitalize first letter)
        size = int(parts[-1].split('.')[0])  # Get the size as an integer

        # Process file content to extract execution time and matches count
        with open(file_path, 'r') as file:
            lines = file.readlines()
            matches_count = 0
            execution_time = 0
            matches_instances = 0
            for i in range(0, len(lines), 7):
                matches_line = lines[i + 3]
                execution_time_line = lines[i + 1]
                matches_count += matches_line.count("'w")
                split_line = execution_time_line.split()
                if len(split_line) >= 3:
                    try:
                        execution_time += float(split_line[-2])
                        matches_instances += 1
                    except ValueError:
                        print(f"Skipping invalid execution time in file: {filename}")
                else:
                    print(f"Skipping invalid format in file: {filename}")

            # Calculate averages
            average_matches = matches_count / matches_instances if matches_instances > 0 else 0
            average_execution_time = execution_time / matches_instances if matches_instances > 0 else 0

            # Store data by model and size
            data[model][size].append((average_execution_time, average_matches))

# Print the table
print("Model | Size | Average Execution Time | Average Stable Matching")
for model, sizes in data.items():
    for size, values in sorted(sizes.items()):
        avg_exec_time = sum(v[0] for v in values) / len(values)
        avg_matches = sum(v[1] for v in values) / len(values)
        print(f"{model} | {size} | {avg_exec_time:.4f} | {avg_matches:.4f}")
