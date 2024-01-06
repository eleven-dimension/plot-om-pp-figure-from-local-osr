import os
import re
import sys
import requests
import json

from tqdm import tqdm
from typing import List

from osrparse import Replay, GameMode

OSR_FILE_PATH_PREFIX = "D:/Software/osu/Data/r/"

def calc_pp_for_single_replay(
    difficulty_rating: float, 
    n320: int, n300: int, n200: int, n100: int, n50: int,  n0: int
) -> float:
    notes = n320 + n300 + n200 + n100 + n50 + n0
    pp_max = (max(difficulty_rating - 0.15, 0.05)) ** 2.2 * (1 + 0.1 * min(1, notes / 1500)) * 8
    acc = ((320 * n320 + 300 * n300 + 200 * n200 + 100 * n100 + 50 * n50) / (320 * notes))
    
    return pp_max * (acc - 0.8) * 5


def parse(osr_file_path):
    r = Replay.from_path(osr_file_path)
    print(r.mods)
    print(r.timestamp)

    # pp = calc_pp_for_single_replay(
    #     difficulty_rating=3.98646,
    #     n320=r.count_geki,
    #     n300=r.count_300,
    #     n200=r.count_katu,
    #     n100=r.count_100,
    #     n50=r.count_50,
    #     n0=r.count_miss
    # )
    # print(pp)

parse(
    OSR_FILE_PATH_PREFIX + "04da4cf11bc0b8fc7df9711a62a848ec-133478026960893621.osr"
)

