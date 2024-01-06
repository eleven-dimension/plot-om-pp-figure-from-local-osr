import os
import re
import sys
import requests
import json
from datetime import datetime

from tqdm import tqdm
from typing import List

from osrparse import Replay, GameMode


API_URL_PREFIX = "https://osu.ppy.sh/api/get_beatmaps?k=b03936ca56264f6a08f27637229aa18ef04fa707&h="
OSR_FILE_PATH_PREFIX = "D:/Software/osu/Data/r/"

dict_from_md5_to_difficulty = {}
replay_records = []


def get_beatmap_md5(osr_file_path: str) -> str:
    match = re.search(r'/r/([^-.]+)', osr_file_path)
    if match:
        return match.group(1)
    else:
        return None
    

def get_beatmap_difficulty(md5: str, mods: int) -> float:
    if (md5, mods) in dict_from_md5_to_difficulty:
        return dict_from_md5_to_difficulty[(md5, mods)]
    
    try:
        response = requests.get(API_URL_PREFIX + md5 + "&mods=" + str(mods))
        if response.status_code == 200:
            data = response.json()

            # unranked or std
            if len(data) == 0 or int(data[0]["approved"]) != 1 or int(data[0]["mode"]) != 3:
                return -1
            
            difficulty_rating = float(data[0]["difficultyrating"])
            
            if difficulty_rating < 0.1:
                print(API_URL_PREFIX + md5 + "&mods=" + str(mods))
                print(data)
                sys.exit(-1)

            dict_from_md5_to_difficulty[(md5, mods)] = difficulty_rating
            return difficulty_rating
        else:
            print(f"error code: {response.status_code}")
    except requests.RequestException as e:
        print(f"error: {e}")
    sys.exit(-1)


def calc_pp_for_single_replay(
    difficulty_rating: float, 
    n320: int, n300: int, n200: int, n100: int, n50: int,  n0: int
) -> float:
    notes = n320 + n300 + n200 + n100 + n50 + n0
    pp_max = (max(difficulty_rating - 0.15, 0.05)) ** 2.2 * (1 + 0.1 * min(1, notes / 1500)) * 8
    acc = ((320 * n320 + 300 * n300 + 200 * n200 + 100 * n100 + 50 * n50) / (320 * notes))
    
    return pp_max * (acc - 0.8) * 5


def get_osr_file_list(osr_file_folder_path: str) -> List[str]:
    osr_files = []

    if os.path.exists(osr_file_folder_path) and os.path.isdir(osr_file_folder_path):
        for file in os.listdir(osr_file_folder_path):
            file_path = os.path.join(osr_file_folder_path, file)

            if os.path.isfile(file_path) and file.lower().endswith('.osr'):
                osr_files.append(file_path)

    return osr_files


def append_a_record(osr_file_path: str) -> None:
    replay = Replay.from_path(osr_file_path)

    # mania
    if replay.mode is not GameMode.MANIA:
        return

    # nf or 4key mod
    mods = replay.mods
    if ((mods >> 15) & 1) == 1 or ((mods >> 1) & 1) == 1:
        return
    
    # ht or dt
    speed_mark = 0
    if ((mods >> 6) & 1) == 1:
        speed_mark = 2
    if ((mods >> 8) & 1) == 1:
        speed_mark = 1
    
    md5 = get_beatmap_md5(osr_file_path)

    # dt
    if speed_mark == 2:
        difficulty_rating = get_beatmap_difficulty(md5, 64)
    # ht
    elif speed_mark == 1:
        difficulty_rating = get_beatmap_difficulty(md5, 256)
    else:
        difficulty_rating = get_beatmap_difficulty(md5, 0)
    # unranked
    if difficulty_rating == -1:
        return
    
    pp = calc_pp_for_single_replay(
        difficulty_rating=difficulty_rating,
        n320=replay.count_geki,
        n300=replay.count_300,
        n200=replay.count_katu,
        n100=replay.count_100,
        n50=replay.count_50,
        n0=replay.count_miss
    )
    if pp <= 0:
        return
    if pp < 10 and replay.timestamp > datetime.fromisoformat("2023-06-01 00:00:00.567256+00:00"):
        print("-------------------------------")
        print("error")
        print(replay.timestamp, pp, md5, speed_mark)
        print(difficulty_rating)
        print(mods)
        return
    # print((replay.timestamp, pp))
    replay_records.append((replay.timestamp, pp, md5, speed_mark))


def add_all_records() -> None:
    osr_file_list = get_osr_file_list(OSR_FILE_PATH_PREFIX)
    # cnt = 0
    for osr_file in tqdm(osr_file_list):
        append_a_record(osr_file)
        # cnt += 1

        # if cnt > 15:
        #     break


if __name__ == "__main__":
    # print(get_osr_file_list("D:/Software/osu/Data/r/"))
    # print(get_beatmap_md5("D:/Software/osu/Data/r/ffc7fc905d6bbe9d10923c43bc6e1bca-133449402616343144.osr"))

    # print(get_beatmap_difficulty("ffc7fc905d6bbe9d10923c43bc6e1bca"))
    # print(dict_from_md5_to_difficulty)

    # print(
    #     calc_pp_for_single_replay(4.01, 522, 603, 139, 9, 2, 4)
    # )

    # append_a_record("D:/Software/osu/Data/r/2202d399e292e1a9559fab14614125ea-133458685956014305.osr")
    # print(replay_records)

    add_all_records()
    print(len(replay_records))

    sorted_records = sorted(replay_records)

    # print(sorted_records)

    file_path = 'sorted_tuple.json'
    with open(file_path, 'w') as file:
        json.dump(sorted_records, file, default=str)