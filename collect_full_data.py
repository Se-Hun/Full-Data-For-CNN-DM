import os
import re

import requests
from tqdm.auto import tqdm
from bs4 import BeautifulSoup

from common.utils import load_txt, dump_json, prepare_dir

def get_title(url):
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.select_one("#cnnHeaderLeftCol > h1")
        if title is None: # for another styles
            title = soup.select_one("body > div.pg-right-rail-tall.pg-wrapper > article > div.l-container > h1")

        title = title.get_text().strip()

    except requests.exceptions.Timeout as errd:
        print("Timeout Error : ", errd)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting : ", errc)
    except requests.exceptions.HTTPError as errb:
        print("Http Error : ", errb)
    except requests.exceptions.RequestException as erra:
        print("AnyException : ", erra)

    return title

def get_date_at_url(url):
    url_segments = url.split("/")
    date_elements = []
    for segment in url_segments:
        try:
            int(segment)
            date_elements.append(segment)
        except:
            continue
    date_string = "-".join(date_elements)
    return date_string

def collect_full_data(fns, mode):
    in_text_data_fn = fns["input"][mode]["text"]
    in_abs_summary_data_fn = fns["input"][mode]["abs"]
    in_url_data_fn = fns["input"][mode]["url"]

    text_data = load_txt(in_text_data_fn)
    abs_data = load_txt(in_abs_summary_data_fn)
    url_data = load_txt(in_url_data_fn)

    assert (len(text_data) == len(abs_data)), "The number of text and abstractive summary does not match !"
    assert (len(text_data) == len(url_data)), "The number of text and url does not match !"

    new_data = []
    for text, abs, url in tqdm(zip(text_data, abs_data, url_data), total=len(text_data)):
        # meta informations
        title = get_title(url)
        date = get_date_at_url(url)
        assert (len(date.split("-")) == 3), "Date is not valid !"

        # article text
        text = text.strip()

        # summaries
        abs = re.sub("<t>", "", abs)
        abs = re.sub("</t>", "", abs)
        abs = abs.strip()

        ext = "" # TODO : Add Ext

        # Save !
        new_data.append({
            "text" : text,
            "title" : title,
            "date" : date,
            "abstractive_summary" : abs,
            "extractive_summary" : ext
        })

    out_fn = fns["output"][mode]
    dump_json(out_fn, new_data)


if __name__ == '__main__':
    harvard_data_dir = os.path.join("./", "harvardnlp_data")
    url_data_dir = os.path.join("./", "url_list")

    result_dir = os.path.join("./", "full_cnn_dm")
    prepare_dir(result_dir)

    fns = {
        "input" : {
            "train" : {
                "text" : os.path.join(harvard_data_dir, "train.txt.src"),
                "abs" : os.path.join(harvard_data_dir, "train.txt.tgt.tagged"),
                "url" : os.path.join(url_data_dir, "all_train.txt")
            },
            "val": {
                "text": os.path.join(harvard_data_dir, "val.txt.src"),
                "abs": os.path.join(harvard_data_dir, "val.txt.tgt.tagged"),
                "url": os.path.join(url_data_dir, "all_val.txt")
            },
            "test": {
                "text": os.path.join(harvard_data_dir, "test.txt.src"),
                "abs": os.path.join(harvard_data_dir, "test.txt.tgt.tagged"),
                "url": os.path.join(url_data_dir, "all_test.txt")
            }
        },
        "output" : {
            "train" : os.path.join(result_dir, "train.json"),
            "val" : os.path.join(result_dir, "val.json"),
            "test" : os.path.join(result_dir, "test.json")
        }
    }

    collect_full_data(fns, "train")
    collect_full_data(fns, "val")
    collect_full_data(fns, "test")