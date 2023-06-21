import csv
import os
import re
directory = "Results/SummaryData/"

def check_csv(algo_type):
    if not os.path.exists(directory+algo_type+'.csv'):
        # CSV file does not exist, create it
        with open(directory+algo_type+'.csv', 'w', newline='') as file:
            # Create an empty CSV file
            writer = csv.writer(file)
            writer.writerow(["parameters",'Easy_0.5','Easy_0.7','Easy_0.9', 'Medium_0.5', 'Medium_0.7', 'Medium_0.9', 'Hard_0.5', 'Hard_0.7', 'Hard_0.9'])


def write(solutions):
    for algoType in solutions:
        for parameters in solutions[algoType]:
            lst_parameters = parameters.split("_")
            percentage = lst_parameters[-1]
            level = lst_parameters[-2]
            other_parameters = lst_parameters[:-2]
            new_filename = directory+algoType+'.csv'
            check_csv(algoType)
            write_to_csv(algoType , other_parameters ,level, percentage,solutions[algoType][parameters] )

def write_to_csv(algo_type , parameters , level, percentage, new_value):
    # Read the existing CSV file
    data = []
    row_index = -1
    column_index = -1
    with open(directory+algo_type+'.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        for row_number, row in enumerate(data):
            if row[0] == str(parameters):
                row_index = row_number
                break

    # Find the index of the column value
    column_index = data[0].index(level+"_"+percentage)

    if row_index==-1:
        # Write the updated data back to the CSV file
        with open(directory + algo_type + '.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            row = ['' for x in range(len(data[0]))]
            row[0]= str(parameters)
            row[column_index]=str(new_value)
            writer.writerow(row)

    # Update the value in the CSV file
    if row_index != -1 and column_index != -1:
        data[row_index][column_index] = str(new_value)
        with open(directory + algo_type + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)



    print(f"Data written to {algo_type} {level} {percentage}  successfully!")
