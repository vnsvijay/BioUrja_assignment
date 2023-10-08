import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

def initialize():
    pass

def swap_elements(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def should_continue():
    while True:
        user_input = input("Press Enter to continue or type 'q' to quit: ").strip()
        if not user_input:
            return True  # User pressed Enter to continue
        elif user_input.lower() == 'q':
            return False  # User typed 'q' to quit

def calculate_region_statistics(data_objects):
    west_sum = 0
    east_sum = 0
    south_sum = 0
    north_sum = 0

    for obj in data_objects:
        first_char = obj["id"][0]

        if first_char == 'E':
            east_sum += obj["forecast"]
        elif first_char == 'N':
            north_sum += obj["forecast"]
        elif first_char == 'W':
            west_sum += obj["forecast"]
        elif first_char == 'S':
            south_sum += obj["forecast"]

    total = west_sum + east_sum + south_sum + north_sum

    west_region = (west_sum * 100) / total
    east_region = (east_sum * 100) / total
    south_region = (south_sum * 100) / total
    north_region = (north_sum * 100) / total

    target_west = 2000
    target_east = 2800
    target_south = 6500
    target_north = 1500
    total_ori = target_east + target_north + target_south + target_west

    ori_west = (target_west * 100) / total_ori
    ori_east = (target_east * 100) / total_ori
    ori_south = (target_south * 100) / total_ori
    ori_north = (target_north * 100) / total_ori

    diff_east = ori_east - east_region
    diff_west = ori_west - west_region
    diff_south = ori_south - south_region
    diff_north = ori_north - north_region
    curr_per_diff = abs(diff_west) + abs(diff_east) + abs(diff_south) + abs(diff_north)

    print("Difference East", diff_east)
    print("Difference West", diff_west)
    print("Difference South", diff_south)
    print("Difference North", diff_north)
    print(f"West Region Sum: {west_sum} west Original Sum:{ori_west}")
    print(f"WEST % contribution: {west_region}")
    print(f"East Region Sum: {east_sum} east Original Sum:{ori_east}")
    print(f"EAST % contribution: {east_region}")
    print(f"North Region Sum: {north_sum} north Original Sum:{ori_north}")
    print(f"NORTH % contribution: {north_region}")
    print(f"South Region Sum: {south_sum} south Original Sum:{ori_south}")
    print(f"SOUTH % contribution: {south_region}")
    print(f"Total: {total}")

    if curr_per_diff >= PERCENTAGE_DIFFERENCE_RATIO_LIMIT * 4:
        print(Fore.RED + Style.BRIGHT + "FAILED RATIO MISMATCH")
    else:
        print(Fore.GREEN + Style.BRIGHT + "SUCCESSFUL!!!!")
    print(Style.RESET_ALL)

def generate_permutations(arr, start=0):
    if start == len(arr) - 1:
        yield arr.copy()
    else:
        for i in range(start, len(arr)):
            swap_elements(arr, start, i)

            yield from generate_permutations(arr, start + 1)

def validate(data_structure, cur_sum):
    if cur_sum >= 12000 - LIMIT and cur_sum <= 12000 + LIMIT:
        table = PrettyTable()
        table.field_names = data_structure[0].keys()

        for row in data_structure:
            table.add_row(row.values())
        print(table)
        print(cur_sum)
        calculate_region_statistics(data_structure)
        if not should_continue():
            return False
    return True

init()
csv_file_path = "input_data.csv"
data = pd.read_csv(csv_file_path)
data_structure = []

for row in data.values:
    data_structure.append({"id": row[0], "weight": row[1] / row[2], "forecast": row[1], "capacity": row[2]})

ids = [item['id'] for item in data_structure]
capacities = [item['capacity'] for item in data_structure]
cur_forecast_sums = []

LIMIT = int(input("Enter the range in which you want to keep it valid. Eg: Enter 500 for +/- 500 from 12000 (recommended 150): "))
PERCENTAGE_DIFFERENCE_RATIO_LIMIT = int(input("Enter the range in which you want to keep percentage ratio of N,E,W,S. Eg: Enter 5 for 5% error margin (recommended 8%): "))

for perm in generate_permutations(capacities):
    cur_forecast_sum = 0
    for i in range(len(perm)):
        data_structure[i]["capacity"] = perm[i]
        data_structure[i]["forecast"] = data_structure[i]["weight"] * perm[i]
        cur_forecast_sum += data_structure[i]["weight"] * perm[i]
    cur_forecast_sums.append(cur_forecast_sum)
    out = validate(data_structure, cur_forecast_sum)
    if not out:
        plt.plot(cur_forecast_sums)
        plt.show()
        df = pd.DataFrame(data_structure)
        df.to_csv("output_data.csv", index=False)
        break
