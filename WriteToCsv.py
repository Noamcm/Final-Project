import csv
import os
import re
directory = "/SummaryData/"

def check_csv(file_name):
    if not os.path.exists(directory+file_name):
        # CSV file does not exist, create it
        with open(directory+file_name, 'w', newline='') as file:
            # Create an empty CSV file
            writer = csv.writer(file)
            writer.writerow(['','Easy', 'Medium', 'Hard'])
            writer.writerow(['0.5','', '', ''])
            writer.writerow(['0.7','', '', ''])
            writer.writerow(['0.9','', '', ''])


def write(file_name ,level_name, algo_types , clique_size):
    level = split_string(level_name)
    new_filename = algo_types+file_name
    print(new_filename , level[0], level[1]  , clique_size)
    check_csv(new_filename)
    write_to_csv(new_filename ,level[0], level[1],clique_size )

def write_to_csv(file_name, column_value, row_value, new_value):
    # Read the existing CSV file
    data = []
    with open(directory+file_name, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Find the index of the column value
    column_index = data[0].index(column_value)

    # Find the index of the row value
    row_index = -1
    for i in range(len(data)):
        if data[i][0] == row_value:
            row_index = i
            break

    # Update the value in the CSV file
    if row_index != -1 and column_index != -1:
        data[row_index][column_index] = str(new_value)

    # Write the updated data back to the CSV file
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Data written to {file_name} successfully!")

def split_string(string):
    # Define the pattern for splitting the string
    pattern = r'(\D+)(\d+\.\d+)_'

    # Use regular expression to split the string
    match = re.match(pattern, string)

    if match:
        # Extract the matched groups
        groups = match.groups()
        return [groups[0], groups[1]]

    # Return None if no match is found
    return None
