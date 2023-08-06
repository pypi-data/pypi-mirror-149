#!/usr/bin/env python3
# type: ignore
import click
import dominate  # type: ignore
from dominate.tags import *
import glob
import json
import os
from typing import Any, Dict, List
import sys
import logging
from pathlib import Path

scripts_dir_path = Path(__file__).parent.parent.resolve()  # one directory up
sys.path.insert(0, str(scripts_dir_path))
from Shared.certoraLogging import logging_setup

logger = logging.getLogger("present_stats")


def create_doc() -> dominate.document:
    doc = dominate.document(title='Stats')

    with doc.head:
        # Bootstrap 4
        link(rel="stylesheet",
             href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
             crossorigin="anonymous",
             integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
             )
    return doc


def table_cell(row: dominate.tags.tr, val: bool) -> None:
    if val is True:
        row.add(td(cls="bg-success"))
    else:
        row.add(td(cls="bg-danger"))


def create_table(data: Dict[str, Any]) -> dominate.tags.div:
    wrapping_div = div(cls="mb-3")
    t = table(cls="table table-bordered w-auto")
    # table header
    with t.add(thead(cls="font-weight-bold")):
        row = tr()
        for elem in data.keys():
            if type(data[elem]) == list:
                row.add(td(elem, colspan=len(data[elem])))
            else:
                row.add(td(elem))
    # table body
    with t.add(tbody()):
        row = tr()
        for _, val in data.items():
            if type(val) == list:
                for v in val:
                    table_cell(row, v)
            else:
                table_cell(row, val)

    wrapping_div += t
    return wrapping_div


def write_html(doc: dominate.document, file_name: Path = Path("stats.html")) -> None:
    print(f"Creating file: {file_name.resolve()}")
    with file_name.open("w") as f:
        f.write(doc.render())


def find_stats_files(work_dir: str) -> List[str]:
    files = glob.glob(work_dir + "/**/statsdata*.json", recursive=True)
    return files


def table_section(inner_div: dominate.tags.div, results: Dict[str, Any], txt: str, op: str) -> None:
    inner_div.add(h5(txt + op))
    inner_div.add(create_table(results))


@click.command()
@click.option('-tn', '--test-name', default=os.getenv("CIRCLE_JOB", "test"), help='test name from CIRCLECI')
@click.option('-wd', '--work-dir', default=".", help='working directory')
def main(test_name: str, work_dir: str) -> None:
    """Create HTML stats file for all the statsdata files in test-name"""
    stats_files = find_stats_files(work_dir)

    if len(stats_files) == 0:
        logger.warning("couldn't find stats files. Skipping")
        sys.exit(0)

    doc = create_doc()

    inner_div = doc.add(div(cls='container'))
    inner_div.add(h1("Statistics - " + test_name))

    for stats_file in stats_files:
        with open(stats_file) as f:
            data = json.load(f)
            try:
                analysis = sorted(data["ANALYSIS"].items())
            except KeyError:
                logger.warning(f"statistic file {stats_file} does not contain ANALYSIS key")
                continue

        inner_div.add(h4("Filename: " + stats_file))
        inner_div.add(hr())
        op = None
        results = {}
        for stats_name, entries in analysis:
            for func_or_cls_name, value in entries.items():
                results[func_or_cls_name] = value
            table_section(inner_div, results, "Parameter name: ", stats_name)
            op = stats_name
            results = {}

    write_html(doc, Path("statistics.html"))


'''
Arguments:
* test_name - default is {CIRCLE_JOB}
* working_directory - default is "."
'''
if __name__ == "__main__":
    logging_setup()
    main()
