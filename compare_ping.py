import re
import csv
import os
from typing import List

TIME_REGEX = re.compile(r"(.*?)time (\d+)ms")
RTT_REGEX = re.compile(r"rtt min/avg/max/mdev = (.*) ms")


def sanitize_runtime(runtime_data: List[str]) -> List[float]:
    def get_time(d):
        match = re.search(TIME_REGEX, d)
        if not match:
            print(f"Runtime REGEX unmatched for {d=}")
            return None
        error, time = match.groups()
        if error:
            print(error)
        return float(time)

    return list(map(get_time, runtime_data))


def sanitize_rtt(rtt_data: List[str]) -> List[str]:
    def get_rtt(rtt):
        match = re.search(RTT_REGEX, rtt)
        if not match:
            print(f"RTT REGEX not matched for {rtt=}")
            return None
        time = match.groups()[0]
        return time

    return list(map(get_rtt, rtt_data))


def get_rtt_data(rtt: str) -> List[float]:
    return list(map(lambda d: float(d), rtt.split("/")))


def append_to_dataset(low_rtt: List[str], high_rtt: List[str]):
    csv_output_file = "output.csv"

    if os.path.getsize(csv_output_file) == 0:
        HEADINGS = [
            [
                "low_min",
                "low_avg",
                "low_max",
                "low_std",
                "high_min",
                "high_avg",
                "high_max",
                "high_std",
            ]
        ]
        with open(csv_output_file, mode="w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([])

            for heading in HEADINGS:
                csv_writer.writerow(heading)

    DATA = []
    for i in range(len(low_rtt)):
        data = get_rtt_data(low_rtt[i])
        data.extend(get_rtt_data(high_rtt[i]))
        DATA.append(data)

    with open(csv_output_file, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in DATA:
            csv_writer.writerow(row)


def compare_rtt(low_rtt: List[str], high_rtt: List[str]):
    print(f"-------------------")

    l = len(low_rtt)
    if l != len(high_rtt) or l == 0:
        print("Length error")
        return None

    min_count, avg_count, max_count = 0, 0, 0

    sum_low_avg, sum_high_avg = 0.0, 0.0

    for i in range(l):
        low_min, low_avg, low_max, _ = get_rtt_data(low_rtt[i])
        high_min, high_avg, high_max, _ = get_rtt_data(high_rtt[i])

        sum_low_avg += low_avg
        sum_high_avg += high_avg

        if low_min >= high_min:
            min_count += 1
        if low_avg >= high_avg:
            avg_count += 1
        if low_max >= high_max:
            max_count += 1

    print(f"Higher low PCP's min RTT: {min_count}/{l}\n")
    print(f"Higher low PCP's avg RTT: {avg_count}/{l}\n")
    print(f"Higher low PCP's max RTT: {max_count}/{l}\n")

    print(f"Avg difference {round(sum_low_avg - sum_high_avg, 3)}ms")
    print(f"-> {round((sum_low_avg - sum_high_avg)/l, 4)}ms per round\n")


def compare_runtime(low_rt: List[float], high_rt: List[float]):
    print(f"-------------------")

    l = len(low_rt)
    if l != len(high_rt):
        print("Length error")
        return None
    count = 0
    equal_count = 0
    for i in range(l):
        if low_rt[i] > high_rt[i]:
            count += 1
        elif low_rt[i] == high_rt[i]:
            equal_count += 1
    print(f"Higher low PCP's runtime: {count}/{l}\n")
    print(f"Equal runtime: {equal_count}/{l}\n")


def read_data():
    def _read_from_file(file_name: str):
        with open(file_name, "r") as file:
            lines = file.read().splitlines()

            run_time_data = sanitize_runtime(lines[0::3])

            rtt_data = sanitize_rtt(lines[1::3])
        return run_time_data, rtt_data

    low_run_time_data, low_rtt_data = _read_from_file("low.txt")
    high_runtime_data, high_rtt_data = _read_from_file("high.txt")

    compare_runtime(low_run_time_data, high_runtime_data)
    compare_rtt(low_rtt_data, high_rtt_data)
    append_to_dataset(low_rtt_data, high_rtt_data)


read_data()
