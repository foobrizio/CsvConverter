class TimeManager:

    def __init__(self, time_setting: int):
        self.cur_hour = "00"
        self.cur_minute = "00"
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
        return f"{self.cur_hour}-{self.calculate_next_hour()}"

    def calculate_next_hour(self) -> str:
        hour_to_int = int(self.cur_hour)
        new_hour = hour_to_int + 1
        if new_hour < 10:
            return "0" + str(new_hour)
        return str(new_hour)