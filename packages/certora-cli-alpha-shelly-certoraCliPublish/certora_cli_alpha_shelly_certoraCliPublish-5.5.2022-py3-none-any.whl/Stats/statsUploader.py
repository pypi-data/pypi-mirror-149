#!/usr/bin/env python3
import click
import glob
import json
import multiprocessing as mp
import pymongo
import sys
from datetime import datetime
from functools import partial
from typing import Any, Dict, List, Tuple, Generator


# takes a list and integer n as input and returns generator objects of n lengths from that list
def chunks(l: List[Any], n: int = 10) -> Generator[List[Any], None, None]:
    for i in range(0, len(l), n):
        yield l[i:i + n]

def upload_stats(mongoPath: str, circleData: Dict[str, Any], stats_file_list: List[str]) -> int:
    client = pymongo.MongoClient(mongoPath)

    db = client.statistics
    collection = db['data']

    statsdata = []

    for filename in stats_file_list:
        file_data = {}
        with open(filename, "r") as rfile:
            file_data = json.load(rfile)
            file_data.update(circleData)
            file_data["path"] = filename
            file_data["insert_time"] = datetime.utcnow()
        statsdata.append(file_data)

    # ordered = False:
    # documents will be inserted on the server in arbitrary order,
    # possibly in parallel, and all document inserts will be attempted.
    try:
        result = collection.insert_many(statsdata, ordered=False)
    except pymongo.errors.PyMongoError as e:
        print(e)
        client.close()
        return 0

    if len(result.inserted_ids) != len(stats_file_list):
        print("Error: There were some files that were not added to db")

    client.close()
    return len(result.inserted_ids)

def find_stats_files(work_dir: str) -> List[str]:
    files = glob.glob(work_dir + "/**/statsdata*.json", recursive=True)
    return files


@click.command()
@click.option('--user', envvar='MONGO_USER')
@click.option('--pwd', envvar='MONGO_PWD')
@click.option('-wd', '--work-dir', default=".", help='working directory')
@click.argument('circleData', nargs=-1)
def main(user: str, pwd: str, work_dir: str, circledata: Tuple[str, ...]) -> None:
    """Store CIRCLEDATA and statsdata in mongoDB"""
    CIRCLECI_DATA = {}  # type: Dict[str, Any]
    # print(circledata)
    try:
        for key_val in circledata:
            key, val = key_val.split("=")
            if key == "pipeline_num" or key == "circle_node_index":
                CIRCLECI_DATA[key] = int(val)
            else:
                CIRCLECI_DATA[key] = val
            # print("k",key,"v",val)
    except ValueError as e:
        print(e)
        sys.exit(1)

    stats_files = find_stats_files(work_dir)

    if len(stats_files) == 0:
        print("Warning: couldn't find stats files. Skipping")
        sys.exit(0)

    pool_size = min(mp.cpu_count(), 4)  # CircleCI declares 2, but detection reads 36
    # pool object creation
    pool = mp.Pool(pool_size)

    mongoPath = "mongodb+srv://{}:{}@basic-vaas-lsi5n.mongodb.net/statistics"\
        "?retryWrites=true&w=majority".format(user, pwd)

    upload_stats_partial = partial(upload_stats, mongoPath, CIRCLECI_DATA)
    # partial function creation for sending all the required CIRCLECI data to upload_stats()

    result = pool.map(upload_stats_partial, chunks(stats_files))
    # creates chunks of 10 filenames
    pool.close()

    found = len(stats_files)
    uploaded = sum(result)
    if uploaded == found:
        print("All found statsdata files ({}) were uploaded to database".format(found))
    else:
        print("Error: {} statsdata files were found and {} were saved into database".format(found, uploaded))
        sys.exit(1)

'''
Arguments:
* working_directory - default is "."
* circle_data - "key=value" "key=value"
'''
if __name__ == "__main__":
    main()
