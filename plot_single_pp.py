import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

import json
import os

file_path = "sorted_tuple.json"

play_time_list, pps = [], []

with open(file_path, 'r') as file:
    data = json.load(file)
    for record in data:
        [play_time_str, pp, md5, mark] = record
        datetime_object = datetime.fromisoformat(play_time_str)
        play_time_list.append(datetime_object)
        pps.append(pp)


plt.scatter(play_time_list, pps, color='blue', marker='o')
plt.show()