import argparse
import os
from typing import Dict, Any
import sys
import re
import json
import shlex
from pathlib import Path
import logging

scripts_dir_path = Path(__file__).parent.parent.resolve()  # one directory up
sys.path.insert(0, str(scripts_dir_path))

from Shared.certoraUtils import change_working_directory
from certoraRun import run_certora

conf_logger = logging.getLogger("conf")
conf_logger.addHandler(logging.StreamHandler(stream=sys.stdout))
conf_logger.setLevel(logging.WARNING)


def type_script(path: str) -> str:
    file_path = Path(path)
    if not file_path.suffix == ".sh":
        raise argparse.ArgumentTypeError(f"File provided must be a shell script file, instead got {path}")
    if not file_path.is_file():
        raise argparse.ArgumentTypeError(f"File {path} not found")
    if not os.access(path, os.X_OK):
        raise argparse.ArgumentTypeError(f"no execute permission for script file {path}")
    return path


def __get_args() -> argparse.Namespace:
    """
    @return: argparse.ArgumentParser with all relevant option arguments, types and logic
    """
    parser = argparse.ArgumentParser(prog="This test gets another test and checks whether using a .conf file produces "
                                          "the same results.", allow_abbrev=False)
    parser.add_argument('file', type=type_script, nargs=1,
                        help='Path to an .sh file we should verify the consistency of when used with a CONF file')

    optional_args = parser.add_argument_group("optional arguments")
    optional_args.add_argument("--debug", action='store_true', help="Use this flag to see debug prints")

    return parser.parse_args()


def get_run_results(script_dir: Path) -> Dict[str, dict]:
    res_dir = None
    max_ctime = 0  # type: float

    for path in script_dir.iterdir():
        if path.is_dir() and re.search(r'emv-\d+-certora-\d{2}-[A-Z][a-z]+--\d{2}-\d{2}', path.name):
            curr_ctime = path.stat().st_ctime
            if curr_ctime > max_ctime:
                res_dir = path.name
                max_ctime = curr_ctime

    assert res_dir is not None, f"A configuration file was not created in {res_dir}"
    res_dir_path = Path(script_dir) / res_dir
    conf_logger.debug(f"Chosen conf is: {res_dir}")
    assert res_dir_path.is_dir()

    output_file = res_dir_path / "Reports" / "output.json"
    conf_logger.debug(f"Output file for run script is {output_file}")
    assert output_file.exists()
    assert output_file.is_file()
    with output_file.open() as f:
        script_run_results = json.load(f)

    build_file = res_dir_path / "inputs" / ".certora_build.json"
    conf_logger.debug(f"Build file for run script is {build_file}")
    assert build_file.exists()
    with build_file.open() as f:
        script_build = json.load(f)

    results_dict = \
        {
            "file_paths":
                {
                    "build": str(build_file),
                    "output": str(output_file)
                },
            "data":
                {
                    "build": script_build,
                    "output": script_run_results
                }
        }

    return results_dict


def dict_eq(a: dict, b: dict) -> bool:
    """
    Returns whether two dictionaries read from JSON files are equal, when ignoring order inside lists.
    We expect the dictionaries to be deeply nested.
    """
    def sort_recursively(obj: Any) -> Any:
        """
        Recursively sorts all lists inside a dictionary that represents a JSON object.
        This is a prerequisite to be able to compare two dictionaries.
        Dictionaries are altered to be list of (key, value) pairs, so they can be sorted. Therefore, the return value
        does not preserve the form of the object, and should only be used for comparison purposes.
        """
        if isinstance(obj, list):
            return sorted([sort_recursively(member) for member in obj])
        elif isinstance(obj, dict):
            return sorted([(key, sort_recursively(val)) for key, val in obj.items()])
        else:
            return obj

    return sort_recursively(a) == sort_recursively(b)


def main() -> None:
    args = __get_args()

    if args.debug:
        conf_logger.setLevel(logging.DEBUG)

    script_path = args.file[0]
    assert script_path is not None
    conf_logger.debug(f"Input script is {script_path}")
    script_path = Path(script_path).resolve()
    conf_logger.debug(f"Sanitized absolute path of script is {script_path}")

    script_dir = script_path.parent
    conf_logger.debug(f"script dir = {script_dir}")

    with script_path.open() as f:
        raw_run_cmd = f.read()

    conf_logger.debug(f"script contents are:\n{raw_run_cmd}")

    with change_working_directory(script_dir):
        try:
            run_cmd = shlex.split(raw_run_cmd)[1:]  # ignores forward slashes etc.
            run_cmd = [word.strip() for word in run_cmd]  # removes newlines
            if conf_logger.level == logging.DEBUG:
                run_cmd.append('--debug')

            print("running certoraRun.py ", ' '.join(run_cmd), flush=True)
            run_certora(run_cmd, True)

            """
            fetch latest result
            """
            first_run_data = get_run_results(script_dir)

            """
            fetch latest conf file
            """
            conf_dir = script_dir / ".last_confs"
            conf_logger.debug(f".last_confs directory is {conf_dir.resolve()}")
            assert conf_dir.is_dir()

            latest_conf = None
            max_ctime = 0  # type: float

            for conf_file in conf_dir.iterdir():
                if re.search(r"last_conf_\d{1,2}_\d{1,2}_\d{4}__\d{1,2}_\d{1,2}_\d{1,2}\.conf", conf_file.name):
                    curr_ctime = conf_file.stat().st_ctime
                    if curr_ctime > max_ctime:
                        latest_conf = conf_file.name
                        max_ctime = curr_ctime

            assert latest_conf is not None, f"A configuration file was not created in {conf_dir}"
            latest_conf = conf_dir / latest_conf
            conf_logger.debug(f"Chosen conf is: {latest_conf}")
            assert latest_conf.is_file()
            assert os.access(latest_conf, os.R_OK), \
                f"No permission to read the generated configuration file {latest_conf}"

            raw_run_cmd_list = [str(latest_conf)]
            print("running certoraRun.py ", ' '.join(raw_run_cmd_list), flush=True)
            run_certora(raw_run_cmd_list, True)

            second_run_data = get_run_results(script_dir)

            if dict_eq(first_run_data["data"], second_run_data["data"]):
                print("Test passed.")
            else:
                print("Test failed.")
                for file in first_run_data["data"]:
                    assert file in second_run_data["data"]
                    if dict_eq(first_run_data["data"][file], second_run_data["data"][file]):
                        first_file = first_run_data["file_paths"][file]
                        second_file = second_run_data["file_paths"][file]
                        print(f"Found a difference between the original file {first_file} and the rerun from "
                              f"configuration file {second_file}")
                        for field in first_run_data["data"][file]:
                            assert field in second_run_data['data'][file]
                            if dict_eq(first_run_data["data"][file][field], second_run_data['data'][file][field]):
                                print(f"field {field} at script run was:\n{first_run_data['data'][file][field]}\n"
                                      f"at configuration file run was:\n{second_run_data['data'][file][field]}")
                sys.exit(1)

        except Exception:
            print("Test failed: " + str(sys.exc_info()))
            sys.exit(1)


if __name__ == '__main__':
    main()
