import math
import sys  # Reading input parameters
import os  # R/W Filesystem
import csv  # R/W .csv files
import pandas  # another csv reader

from util.CsvReader import CsvReader
from util.TimeManager import TimeManager

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_path():
    input_args = sys.argv
    my_path = input_args[0]
    while True:
        if len(input_args) > 2 and input_args[1] == "-p":
            my_path = input_args[2]
        else:
            my_path = input("Insert path: ")
        correctness = os.path.isdir(my_path)
        if correctness:
            break
    return my_path


def load_csv_files(my_path: str):
    my_csv_files = []
    for my_file in os.listdir(my_path):
        if os.path.splitext(my_file)[-1] == ".csv":
            my_csv_files.append(my_file)
    if len(my_csv_files) == 0:
        print("No .csv file was found inside "+my_path)
        raise Exception()
    print(f"{len(my_csv_files)} files found")
    return my_csv_files


def reduce(csv_file: str, filewriter: object, time_setting: int):
    """
    This method takes a dataset and reduces its rows. The new rows are written in a new file using the writer object
    :param csv_file:
    :param filewriter:
    :param time_setting: It specifies the range of time for merging records: 0 for a quarter of hour, 1 for half hour, 2 for an hour
    :return:
    """
    csv_reader = CsvReader()

    with open(csv_file) as old_dataset:
        cont = 0
        results = pandas.read_csv(old_dataset)
        time_manager = TimeManager(time_setting=time_setting)
        # reader = csv.reader(old_dataset)
        try:
            for i in range(0, len(results)):
                row = results.values[i][0]
                if type(row) is float and math.isnan(row):
                    # We need to skip this row
                    continue
                else:
                    row = row.split(';')
                timestamp = row[0]
                day = timestamp[0:10]
                hour = timestamp[11:13]
                minute = timestamp[13:15]
                if time_manager.time_to_reduce(hour, minute):
                    # Perform the average, update cur_hour and write a new row inside the final dataset
                    write_row_with_average(filewriter=filewriter,
                                           reader=csv_reader,
                                           time_range=time_manager.get_time_range(),
                                           day=day)
                    time_manager.update_time_count(hour, minute)
                    #cur_hour = hour

                # Collect all the data of the hour
                csv_reader.collect_row(row)
        except Exception as e:
            print(cont)
            # We found a _csv Error
            print(e.args)
            if e.args[0] == 'line contains NUL':
                # We are at the end of the file
                write_row_with_average(filewriter=filewriter,
                                       reader=csv_reader,
                                       time_range=time_manager.get_time_range(),
                                       day=day)


def write_row_with_average(filewriter: object, reader: CsvReader, time_range: str, day: str):
    # We are at the end of the file
    new_data = reader.perform_average()
    new_data.insert(0, time_range)
    new_data.insert(0, day)
    filewriter.writerow(new_data)


def write_header(filewriter: object):
    """
    Write the header inside the new .csv file
    :param filewriter:
    :return:
    """
    header = ["date", "time_range", "wind_speed_value", "wind_force", "wind_direction_num", "wind_direction_deg", "humidity",
              "temperature", "noise", "PM2.5", "PM10", "atm_pressure", "light", "light_hundred", "rainfall"]
    writer.writerow(header)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Get path containing all the csv files
    path = get_path()
    #path, time_setting = read_parameters()

    # Eventually delete the previously produced result
    new_file = path + "/final_dataset.csv"
    if os.path.exists(new_file):
        os.remove(new_file)

    # List all .csv files
    files = load_csv_files(path)
    # Create the new .csv file

    f = open(new_file, 'w', newline='')
    writer = csv.writer(f)
    write_header(writer)
    for file in files:
        # For each file of the directory, we'll read the content, reduce it and write a row inside the new file
        reduce(path+"/"+file, writer, 2)
    f.close()

