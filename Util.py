
def calculate_next_hour(hour: str):
    hour_to_int = int(hour)
    new_hour = hour_to_int + 1
    if new_hour < 10:
        return "0"+str(new_hour)
    return str(new_hour)
