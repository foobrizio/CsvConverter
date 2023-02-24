from util.CsvReader import CsvReader


class FinalCsvWriter:

    def __init__(self, filewriter):
        self.writer = filewriter

    def write_row_with_average(self, reader: CsvReader, time_range: str, day: str):
        """
        Performs the average of collected data and writes a new row inside the final file
        """
        # We are at the end of the file
        new_data = reader.perform_average()
        new_data.insert(0, time_range)
        new_data.insert(0, day)
        self.writer.writerow(new_data)

    def write_header(self):
        """
        Write the header inside the new .csv file
        """
        header = ["date", "time_range", "wind_speed_value", "wind_force", "wind_direction_num", "wind_direction_deg",
                  "humidity",
                  "temperature", "noise", "PM2.5", "PM10", "atm_pressure", "light", "light_hundred", "rainfall"]
        self.writer.writerow(header)
