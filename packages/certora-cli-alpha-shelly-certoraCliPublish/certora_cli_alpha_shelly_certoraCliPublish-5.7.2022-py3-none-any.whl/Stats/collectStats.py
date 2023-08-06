#!/usr/bin/env python3

import click
import glob
import json
import itertools
import multiprocessing
import os
import shlex
import subprocess
import sys
import time
from typing import Any, Dict, Generator, Iterable, List, Set
import logging
from pathlib import Path

scripts_dir_path = Path(__file__).parent.parent.resolve()  # one directory up
sys.path.insert(0, str(scripts_dir_path))
from Shared.certoraUtils import output_to_csv
from Shared.certoraLogging import logging_setup

logger = logging.getLogger("stats")

RUN_TOOLS_FIELDNAMES = [
    "id",
    "solc_executable",
    "outputs_s3_bucket",
    "time_started",
    "time_finished",
    "overall_runtime_milliseconds",
    "test_id"
]

CI_JOB_TO_TOOL_RUNS_FIELDNAMES = [
    'ci_job_id',
    'tool_run_id'
]

ci_job_to_tool_runs_ob = {
    "table_name": "ci_job_to_tool_runs",
    "header": CI_JOB_TO_TOOL_RUNS_FIELDNAMES,
    "metadata": [
        {
            "filename": None,
            "mapping": {
                'ci_job_id': {
                    'concatenate': True,
                    'separator': "_",
                    'combination': [
                        {
                            'isVar': True,
                            'name': 'pipeline'
                        },
                        {
                            'isVar': True,
                            'name': 'job_name'
                        }
                    ]
                },
                'tool_run_id': {
                    'table': 'tool_runs',
                    'name': 'id'
                }
            }
        }
    ]
}  # type: Dict[str, Any]

tool_runs_ob = {
    "table_name": "tool_runs",
    "header": RUN_TOOLS_FIELDNAMES,
    "metadata": [
        {
            "filename": "statsdata*.json",
            "mapping": {
                "overall_runtime_milliseconds": "start_to_end_time",  # todo: it may be missing
                "time_started": "start_timestamp",
                "time_finished": "end_timestamp"
            }
        },
        {
            "filename": ".certora_metadata.json",
            "mapping": {
                "solc_executable": "solc"
            }
        },
        {
            "filename": None,
            "mapping": {
                'outputs_s3_bucket': {
                    'concatenate': True,
                    'separator': "/",
                    'combination': [
                        {
                            'isVar': True,
                            'name': 'bucket'
                        },
                        {
                            'isVar': True,
                            'name': 'pipeline'
                        },
                        {
                            'isVar': True,
                            'name': 'job_name'
                        },
                        {
                            'isVar': True,
                            'name': 'emv_path'
                        }
                    ]
                }
            }
        },
        {
            "filename": ".certora_metadata.json",
            "mapping": {
                "id": "timestamp"
            },
            'type': 'timestamp',
            'store': True
        },
        {
            "filename": None,
            "mapping": {
                'test_id': {
                    'json': True,
                    'combination': [
                        {
                            'filename': ".certora_metadata.json",
                            'name': 'cwd_relative'
                        },
                        {
                            'filename': ".certora_metadata.json",
                            'name': 'conf'
                        }
                    ]
                }
            }
        }
    ]
}  # type: Dict[str, Any]

# ORDER matters
obs = [
    tool_runs_ob,
    ci_job_to_tool_runs_ob  # tool_runs.id must be defined
]


def find_files(pattern: str, work_dir: str = "") -> List[str]:
    """
        Looks for file paths that match the pattern in the supplied working directory
    """
    files = glob.glob(work_dir + pattern, recursive=True)
    return files


def get_file(dir_path: str, file_pattern: str) -> str:
    """
        Looks for the file (based on the supplied pattern) in supplied directory path

        @param dir_path: directory path that presumably contains the requested file
        @param file_pattern: file pattern e.g. statsdata*.json or .certora_metadata.json

        @return file_path: empty string if no file was found
    """
    files = glob.glob(f'{dir_path}/{file_pattern}')

    file_path = ''

    if len(files) > 1:  # In case there is more than one ?
        # get the latest file
        files_ctime = [os.path.getctime(f) for f in files]
        ind = files_ctime.index(max(files_ctime))
        file_path = files[ind]
    elif files:  # there is a single file
        file_path = files[0]
    return file_path


def execute(cmd: str) -> None:
    try:
        print(cmd)
        with subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, universal_newlines=True) as p:
            if p.stdout:
                for line in iter(p.stdout.readline, ""):
                    print(line)
    except Exception as e:
        logger.error(f"Could not execute command {cmd} - {e}")


#  Generator[YieldType, SendType, ReturnType]
def grouper(n: int, iterable: Iterable[str]) -> Generator[List, Any, None]:
    """grouper(3, 'ABCDEFG') --> ABC DEF G"""
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def upload_json_files(bucket: str, work_dir: str, pipeline_number: int, circle_job_name: str,
                      current_node_dirs: List[str]) -> None:
    cmd = f'aws s3 sync {work_dir} s3://{bucket}/{pipeline_number}/{circle_job_name}/'
    cmd += ' --exclude "*"'

    # group every 3 output directories
    groups = list(grouper(3, current_node_dirs))
    print(groups)
    commands = []  # type: List[str]

    for group in groups:
        current_cmd = cmd
        for d in group:
            # d looks like Test/{sub_folder/s}/emv-.../ or CustomersCode/{sub_folder/s}/emv-.../
            # remove Test/ (or CustomersCode/) as we run aws sync from this directory (check work_dir)
            current_d = d.replace("Test/", "").replace("CustomersCode/", "")
            current_cmd += f' --include "{current_d}*.json"'
        current_cmd += ' --exclude "*expected.json" --exclude "*package.json" --exclude "*tsconfig.json"'
        commands.append(current_cmd)

    par(commands)


def par(commands: List[str]) -> None:
    try:
        pool_size = min(multiprocessing.cpu_count(), 8)
        with multiprocessing.Pool(pool_size) as pool:
            # submits commands to the process pool as separate tasks
            pool.map(execute, commands)
    except Exception as e:
        print(e)
        sys.exit(1)


def upload_csv_files(bucket: str, pipeline_number: int, circle_job_name: str, csv_files: Set[str] = None) -> None:
    """
        Upload all the files to S3

        @param bucket: S3 bucket name
        @param pipeline_number: CI param
        @param circle_job_name: CI param
        @param csv_files: set of csv filenames
    """
    if csv_files is None or len(csv_files) == 0:
        logger.error("you must supply csv filenames!")
        return
    commands = []
    for csv_file in csv_files:
        commands.append(f'aws s3 cp "{csv_file}.csv" s3://{bucket}/{pipeline_number}/{circle_job_name}/')
    par(commands)


def search_for_attr(d: Dict[str, Any], attr: str) -> Any:
    """
        Search for the attribute in the supplied dictionary

        @param d: dictionary
        @param attr: requested attribute

        @return the value of the requested attribute or None if not found
    """
    if attr in d.keys():
        val = d[attr]
        if type(val) == list:
            return sorted(val)
        elif type(val) == dict:
            return {i: val[i] for i in sorted(val.keys())}
        return val
    for val in d.values():
        if isinstance(val, dict):
            val = search_for_attr(val, attr)
            if val is not None:
                return val
    return None


def get_data(relative_path: str, attrs: Dict[str, str]) -> Dict[str, Any]:
    """
        Reads json file (using the relative_path) and retrieves the requested attributes

        @param relative_path: relative path to the json file (e.g 'Test/Subfolder/.certora_metada.json')
        @param attrs: mapping from the name of the attribute as it appears in the schema to its
        name in the json file (e.g {"solc_executable": "solc"})

        @return: mapping of the requested attributes and their values
    """
    results = {}
    if attrs:
        try:
            with open(f'{relative_path}') as json_file:
                data = json.load(json_file)
                for attr_name, attr in attrs.items():
                    print(f"searching for '{attr}'")
                    val = search_for_attr(data, attr)
                    print(f"found {val}")
                    if val is not None:
                        results[attr_name] = val
        except FileNotFoundError:
            logger.warning(f"Couldn't find {relative_path}")
        except ValueError:
            logger.warning(f"Couldn't parse {relative_path}")

    return results


def is_defined(var_name: str, local_vars: Dict[str, Any]) -> bool:
    if var_name not in local_vars:
        logger.error(f"{var_name} variable is not defined!")
        return False
    return True


def get_timestamp(str_timestamp: str = "") -> int:
    ms_mul = 1000000  # adds 6 digits (representing ms) to timestamp
    if str_timestamp:
        timestamp = int(float(str_timestamp) * ms_mul)
    else:
        timestamp = int(time.time() * ms_mul)
    return timestamp


def get_variable_value(var_name: str, local_variables: Dict[str, Any]) -> Any:
    if is_defined(var_name, local_variables):
        return local_variables[var_name]
    logger.error(f"{var_name} is undefined")
    sys.exit(1)


def get_data_from_file(dir_path: str, filename: str, attrs: Dict[str, str], attr_type: str = "") -> Dict[Any, Any]:
    source_file = get_file(dir_path, filename)
    mapping = {}
    if source_file:
        mapping = get_data(source_file, attrs=attrs)
        if not mapping:
            logger.warning(f"Couldn't find the required attributes {attrs}")
    else:
        logger.warning(f"Couldn't find {filename}")
    # currently timestamp is the only supported type
    if attr_type == 'timestamp':  # for timestamp type len(attrs) must be 1
        if mapping:
            for k, v in mapping.items():
                mapping[k] = get_timestamp(v)
        else:  # if couldn't find the attribute
            for attr_name in attrs.keys():  # get the name of the attribute
                mapping[attr_name] = get_timestamp()
    return mapping


def add_variable(table_name: str, local_variables: Dict[str, Any], var_name: str, var_value: Any) -> None:
    """add this variable to the local_variables dictionary so it can be later retrieved
    it should be stored in the local_variables with {table_name} as a dict and
    attribute_name as its key (local_variables[table_name][var_name])
    """
    if table_name not in local_variables:
        local_variables[table_name] = {}
    local_variables[table_name][var_name] = var_value


@click.command()
@click.option('-b', '--bucket', required=False, default='certora-ci', help='bucket name')
@click.option('-wd', '--work-dir', default=".", help='working directory')
@click.option('-pipe', '--pipeline', required=True, type=int, help='pipeline number')
@click.option('-job', '--job-name', required=True, help='circleci job name')
@click.option('-node', '--node-index', required=True, type=int, help='circle node index')
def main(bucket: str, work_dir: str, pipeline: int, job_name: str, node_index: int) -> None:
    if job_name == 'smart_reg_test':
        sub_folder = 'Test/'
    elif job_name == 'test_customers_code':
        sub_folder = 'CustomersCode/'
    elif job_name == 'test_expensive_customers_code':
        sub_folder = 'CustomersCode/'
    else:
        logger.fatal('Unrecognized job')
        sys.exit(1)
    # search for all the emv- directories
    current_node_dirs = find_files("**/emv-[0-9a-zA-Z-_.]*/", sub_folder)

    local_variables = {}
    local_variables.update(locals())

    csv_files = set()  # type: Set[str]
    defined = {}  # type: Dict[str, bool]

    # for each emv- directory
    for emv_path in current_node_dirs:
        if not os.path.isdir(emv_path):
            logger.warning(f"Invalid directory {emv_path}")
            continue
        local_variables['emv_path'] = emv_path
        dir_path = f'{emv_path}/*/'
        # for each table object
        for ob in obs:
            table_name = ob.get("table_name", "")
            header = ob.get('header', [])
            if len(header) == 0:
                logger.error('missing table header!')
                sys.exit(1)
            # if there is a table that should be defined once for each pipeline
            once = ob.get('once', False)
            if defined.get(table_name, False):
                # already defined
                continue  # to the next table

            if table_name == "":
                logger.error('missing table_name value')
                sys.exit(1)
            results = {}
            metadata = ob.get('metadata', [])

            for attribute_group in metadata:
                if attribute_group.get('filename', None):
                    # look for the file in current emv folder
                    attr_type = attribute_group.get("type", "")
                    mapping = attribute_group.get('mapping', {})
                    attributes_values = get_data_from_file(dir_path,
                                                           attribute_group['filename'],
                                                           mapping,
                                                           attr_type)
                    store = attribute_group.get("store", False)
                    if store:
                        for attr_name, attr_value in attributes_values.items():
                            add_variable(table_name, local_variables, attr_name, attr_value)
                    results.update(attributes_values)
                else:  # filename is None or missing
                    mapping = attribute_group['mapping']
                    data = {}
                    # mapping: { "attribute_name": {} }
                    for name, guide in mapping.items():
                        # guide: { "isVar/concatenate/json": True, ...}
                        # or: {"table": "{table_name}", ... }
                        if guide.get('isVar', False):
                            # guide: { "isVar": True, "name": var_name }
                            value = get_variable_value(guide['name'], local_variables)
                            data[name] = value
                        elif guide.get('concatenate', False):
                            # guide: { "concatenate": True, "separator": "{sep}",  "combination": [{}] }
                            combination = guide.get("combination", [])
                            # combination: list of
                            # { "isVar": True, "name":  var_name }
                            # or { "filename": "", "name": "{file attribute name}", (optional) "type": "timestamp" }
                            sep = guide.get("separator", "")
                            str_comb_result = ''  # concatenation result
                            for elem in combination:
                                if elem.get('isVar', False):
                                    value = get_variable_value(elem['name'], local_variables)
                                    str_comb_result += str(value) + sep
                                elif 'filename' in elem:
                                    attr_type = elem.get("type", "")
                                    dict_value = get_data_from_file(dir_path, elem['filename'],
                                                                    {name: elem['name']}, attr_type)
                                    value = dict_value.get(name, None)
                                    if value is not None:
                                        str_comb_result += str(value) + sep
                            if str_comb_result:
                                # remove the last separator
                                if sep:
                                    str_comb_result = str_comb_result[:-1]
                                if guide.get('store', False):
                                    add_variable(table_name, local_variables, name, str_comb_result)
                                data[name] = str_comb_result
                        elif guide.get('sum', False):
                            # guide: { "sum": True, "combination": [{}] }
                            combination = guide.get("combination", [])
                            # combination: list of
                            # { "isVar": True, "name":  var_name }
                            # or { "filename": "", "name": "{file attribute name}", (optional) "type": "timestamp" }
                            sum_result = 0
                            for elem in combination:
                                if elem.get('isVar', False):
                                    value = get_variable_value(elem['name'], local_variables)
                                    sum_result += int(value)
                                elif 'filename' in elem:
                                    attr_type = elem.get("type", "")
                                    dict_value = get_data_from_file(dir_path, elem['filename'],
                                                                    {name: elem['name']}, attr_type)
                                    value = dict_value.get(name, None)
                                    if value is not None:
                                        sum_result += int(value)
                            if guide.get('store', False):
                                add_variable(table_name, local_variables, name, sum_result)
                            data[name] = sum_result
                        elif 'table' in guide:
                            # guide: { "table": "{table_name}", "name": {table_attribute_name} }
                            table = guide['table']
                            attribute = guide['name']
                            value = local_variables.get(table, {}).get(attribute, None)
                            if value is None:
                                logger.error(
                                    f"couldn't find {table}, {attribute} attribute in local variables. "
                                    f"Make sure you placed {table_name} after {table}"
                                )
                                sys.exit(1)
                            data[name] = value
                        elif 'json' in guide:
                            # guide: { "json": True, "combination": [{}] }
                            combination = guide.get("combination", [])
                            comb_result = {}
                            for elem in combination:
                                if elem.get('isVar', False):
                                    value = get_variable_value(elem['name'], local_variables)
                                    comb_result.update({elem['name']: value})
                                elif 'filename' in elem:
                                    attr_type = elem.get("type", "")
                                    dict_value = get_data_from_file(dir_path, elem['filename'],
                                                                    {elem['name']: elem['name']}, attr_type)
                                    comb_result.update(dict_value)
                            if guide.get('store', False):
                                add_variable(table_name, local_variables, name, comb_result)
                            # default quoting character is double-quote
                            data[name] = json.dumps(comb_result).replace("\\", "").replace('""', '"')
                    results.update(data)
            for attribute in header:
                if attribute not in results.keys():
                    logger.warning(f"There is a missing attribute - {attribute}")
            csv_filename = f"{table_name}_"  # using the same filename prevents duplicates in db
            if not once:
                # create a csv file for each CI node
                csv_filename += f"{node_index}"
            else:
                defined[table_name] = True

            if output_to_csv(csv_filename, header, results):
                csv_files.add(csv_filename)
            else:
                logger.error(f"Couldn't output data to a csv file for {csv_filename}.")

    # upload json files
    upload_json_files(bucket, os.path.join(work_dir, sub_folder), pipeline, job_name, current_node_dirs)
    if csv_files is None or len(csv_files) == 0:
        logger.fatal("you must supply csv filenames!")
        sys.exit(3)  # this will be captured by CI

    # upload csv files
    upload_csv_files(bucket, pipeline, job_name, csv_files)


if __name__ == '__main__':
    logging_setup()
    main()
