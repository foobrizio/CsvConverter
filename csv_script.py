import math
import sys  # Reading input parameters
import os  # R/W Filesystem
import csv  # R/W .csv files
import pandas  # another csv reader
import re  # For regex

from util.CsvReader import CsvReader
from util.FinalCsvWriter import FinalCsvWriter
from util.TimeManager import TimeManager

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def read_parameters():
    input_args = sys.argv
    my_path = "",
    my_time_setting = 2

    # Let's check if parameters contain path
    if input_args.__contains__("-p"):
        my_path_index = input_args.index("-p") + 1
        if len(input_args) <= my_path_index - 1:
            my_path = input_args[my_path_index]
    while True:
        if len(my_path) > 1:
            correctness = os.path.isdir(my_path)
            if correctness:
                break
        my_path = input("Insert path:")

    # Let's check now if parameters contain time_setting
    if input_args.__contains__("-t"):
        my_time_index = input_args.index("-t") + 1
        if len(input_args) <= my_time_index - 1:
            my_time_setting = input_args[my_time_index]

    if my_time_setting < 0 or my_time_setting > 2:
        my_time_setting = 2

    return my_path, my_time_setting


def load_csv_files(my_path: str):
    """
    Here we load all the csv files inside our folder. We want to exclude files that were previously generated by us
    :param my_path:
    :return:
    """
    my_csv_files = []
    for my_file in os.listdir(my_path):
        if os.path.splitext(my_file)[-1] == ".csv":
            my_csv_files.append(my_file)
    if len(my_csv_files) == 0:
        print("No .csv file was found inside "+my_path)
        raise Exception()
    regex = "final_dataset*"
    p = re.compile(regex)
    total_files = [s for s in my_csv_files if not p.match(s)]
    print(f"{len(total_files)} files found")
    return total_files


def reduce(csv_file: str, time_setting: int):
    """
    This method takes a dataset and reduces its rows. The new rows are written in a new file using the writer object
    :param csv_file:
    :param time_setting: It specifies the range of time for merging records: 0 for a quarter of hour, 1 for half hour, 2 for an hour
    :return:
    """
    csv_reader = CsvReader()

    with open(csv_file) as old_dataset:
        results = pandas.read_csv(old_dataset)
        time_manager = TimeManager(time_setting=time_setting)
        try:
            for i in range(0, len(results)):
                row = results.values[i][0]
                if type(row) is float and math.isnan(row):
                    # We need to skip this row because is bad
                    continue
                else:
                    row = row.split(';')
                timestamp = row[0]
                day = timestamp[0:10]
                hour = timestamp[11:13]
                minute = timestamp[14:16]
                if time_manager.time_to_reduce(hour, minute):
                    # Perform the average, update cur_hour and write a new row inside the final dataset
                    final_writer.write_row_with_average(reader=csv_reader,
                                                        time_range=time_manager.get_time_range(),
                                                        day=day)
                    time_manager.update_time_count(hour, minute)

                # Collect all the data of the hour
                csv_reader.collect_row(row)
        except Exception as e:
            # We found a _csv Error
            print(e.args)
            if e.args[0] == 'line contains NUL':
                # We are at the end of the file
                final_writer.write_row_with_average(reader=csv_reader,
                                                    time_range=time_manager.get_time_range(),
                                                    day=day)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Get path containing all the csv files
    path, time_setting = read_parameters()

    # Eventually delete the previously produced result
    new_file = path + "/final_dataset"
    if time_setting == 1:
        new_file += "_half.csv"
    elif time_setting == 0:
        new_file += "_quarter.csv"
    else:
        new_file += "_hour.csv"
    if os.path.exists(new_file):
        os.remove(new_file)

    # List all .csv files
    files = load_csv_files(path)
    # Create the new .csv file

    f = open(new_file, 'w', newline='')
    final_writer = FinalCsvWriter(csv.writer(f))
    final_writer.write_header()
    for file in files:
        # For each file of the directory, we'll read the content, reduce it and write a row inside the new file
        reduce(path+"/"+file, time_setting)
    f.close()
