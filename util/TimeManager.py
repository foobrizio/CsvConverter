class TimeManager:

    def __init__(self, time_setting: int, first_timestamp: str):
        row_hour = first_timestamp[11:13]
        row_minute = int(first_timestamp[14:16])
        self.cur_hour = row_hour
        if time_setting == 2:   # Hourly
            self.cur_minute = "00"
        elif time_setting == 1:     # Half hour
            self.cur_minute = "30" if row_minute >= 30 else "00"
        else:   # Quarter
            if row_minute >= 30:
                self.cur_minute = "45" if int(row_minute) >= 45 else "30"
            else:
                self.cur_minute = "15" if row_minute >= 15 else "00"
        self.time_setting = time_setting

    def time_to_reduce(self, hour: str, minute: str) -> bool:
        """
        Returns true if it's time to merge all the collected rows. It depends on the time_setting.
        Items are collected every hour, half an hour or a quarter of hour
        :param hour: the hour read from the dataset row
        :param minute: the minute read from the dataset row
        :return:
        """
        if self.time_setting == 2:  # Hourly
            return self.cur_hour != hour
        elif self.time_setting == 1:  # Half hour
            return (self.cur_hour != hour) or (int(minute) - int(self.cur_minute) >= 30)
        else:   # Quarter of hour
            return (self.cur_hour != hour) or (int(minute) - int(self.cur_minute) >= 15)

    def update_time_count(self, hour: str, minute: str):
        """
        Updates values for cur_hour and cur_minute
        :param hour: the hour read from the dataset row
        :param minute: the minute read from the dataset row
        """
        if self.time_setting == 1:    # Half hour
            self.cur_minute = "30" if int(minute) >= 30 else "00"
        elif self.time_setting == 0:  # Quarter of hour
            if int(minute) >= 30:
                self.cur_minute = "45" if int(minute) >= 45 else "30"
            else:
                self.cur_minute = "15" if int(minute) >= 15 else "00"
        self.cur_hour = hour

    def get_time_range(self) -> str:
        if self.time_setting == 2:
            return f"{self.cur_hour}-{self.calculate_next_hour()}"
        else:
            starting_point = f"{self.cur_hour}:{self.cur_minute}"
            ending_point = self.calculate_next_minute()
            return f"{starting_point}-{ending_point}"

    def calculate_next_hour(self) -> str:
        hour_to_int = int(self.cur_hour)
        new_hour = (hour_to_int + 1) % 24
        if new_hour < 10:
            return "0" + str(new_hour)
        return str(new_hour)

    def calculate_next_minute(self) -> str:
        hour_to_int = int(self.cur_hour)
        minute_to_int = int(self.cur_minute)
        new_minute = minute_to_int + 30 if self.time_setting == 1 else minute_to_int + 15

        new_hour = hour_to_int
        # We have still to consider the case we are at 23:30/23:45 pm
        if new_minute >= 60:
            new_hour = (new_hour + 1) % 24
            new_minute = 0
        if new_hour < 10:
            new_hour = "0" + str(new_hour)
        if new_minute < 10:
            new_minute = "0" + str(new_minute)
        return f"{new_hour}:{new_minute}"
