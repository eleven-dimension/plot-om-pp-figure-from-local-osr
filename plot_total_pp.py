import matplotlib.pyplot as plt
import json
from datetime import datetime

file_path = "sorted_tuple.json"

dict_from_md5_mode_to_best_pp = {}
dict_of_all_md5 = {}

play_time_list, total_pps = [], []

with open(file_path, 'r') as file:
    data = json.load(file)

    for record in data:
        [play_time_str, pp, md5, mark] = record
        datetime_object = datetime.fromisoformat(play_time_str)

        dict_of_all_md5[md5] = True

        if (md5, mark) in dict_from_md5_mode_to_best_pp:
            current_best_pp = dict_from_md5_mode_to_best_pp[(md5, mark)]
            if current_best_pp >= pp:
                continue
        
        dict_from_md5_mode_to_best_pp[(md5, mark)] = pp

        pp_list = sorted(dict_from_md5_mode_to_best_pp.values())

        # calc total pp
        total_pp = 0
        weight = 1
        for index in range(len(pp_list) - 1, -1, -1):
            # len(pp_list) - 1 -> 1
            rk = len(pp_list) - index
            total_pp += pp_list[index] * weight
            weight *= 0.95
        total_pp += 416.6667 * (1 - 0.9994 ** len(dict_of_all_md5))
        
        # append
        play_time_list.append(datetime_object)
        total_pps.append(total_pp)

    plt.plot(play_time_list, total_pps, marker='o', linestyle='-', color='b')
    plt.show()