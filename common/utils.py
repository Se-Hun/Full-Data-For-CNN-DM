import os
import json

import pandas as pd

def prepare_dir(dir_name):
    if not os.path.exists(dir_name): os.makedirs(dir_name)


def load_json(fn):
    with open(fn, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data

def dump_json(fn, data):
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print("Data file is dumped at ", fn)


def load_json_lines(fn):
    data = []
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data


def load_csv(fn):
    data = pd.read_csv(fn)
    return data

def dump_csv(fn, df):
    df.to_csv(fn, index=False)
    print("Data file is dumped at ", fn)


def load_txt(fn):
    with open(fn, "r", encoding="utf-8") as f:
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line.strip())
        return data

def dump_txt(fn, lines):
    with open(fn, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
        print("Data file is dumped at ", fn)