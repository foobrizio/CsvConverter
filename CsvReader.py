class CsvReader:

    def __init__(self):
        self.wind_speed_sum = 0
        self.wind_dir_sum = 0
        self.wind_dir_degrees_sum = 0
        self.humidity_sum = 0
        self.temperature_sum = 0
        self.noise_sum = 0
        self.pm2_5_sum = 0
        self.pm10_sum = 0
        self.atm_sum = 0
        self.light_sum = 0
        self.light_hum_sum = 0
        self.rain_sum = 0
        self.cont = 0

    def collect_row(self, row: list):
        self.wind_speed_sum += float(row[1])
        self.wind_dir_sum += float(row[2])
        self.wind_dir_degrees_sum += float(row[3])
        self.humidity_sum += float(row[4])
        self.temperature_sum += float(row[5])
        self.noise_sum += float(row[6])
        self.pm2_5_sum += float(row[7])
        self.pm10_sum += float(row[8])
        self.atm_sum += float(row[9])
        self.light_sum += float(row[10])
        self.light_hum_sum += float(row[11])
        self.rain_sum += float(row[12])
        self.cont += 1

    def perform_average(self):
        result = [self.wind_speed_sum / self.cont, self.wind_dir_sum / self.cont, self.wind_dir_degrees_sum / self.cont,
                  self.humidity_sum / self.cont, self.temperature_sum / self.cont, self.noise_sum / self.cont,
                  self.pm2_5_sum / self.cont, self.pm10_sum / self.cont, self.atm_sum / self.cont,
                  self.light_sum / self.cont, self.light_hum_sum / self.cont, self.rain_sum / self.cont]
        self.__init__()
        return result
