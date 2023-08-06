import logging
import click
import json
import re
import shlex
import subprocess
import sys
import time
from junit_xml import TestSuite, TestCase
from tabulate import tabulate
from typing import List, Optional, Tuple, Dict, Any
from pathlib import Path

scripts_dir_path = Path(__file__).parent.parent.resolve()  # one directory up
sys.path.insert(0, str(scripts_dir_path))
from certoraRun import run_certora
from CI_tests.miniTester import compare_results_with_expected, get_errors, get_violations
from Shared.certoraUtils import prepare_call_args, as_posix, is_windows, get_certora_root_directory
from Shared.certoraUtils import BASH_RED_COLOR, BASH_END_COLOR, BASH_GREEN_COLOR, BASH_ORANGE_COLOR
from Shared.certoraUtils import red_text, orange_text, green_text, change_working_directory
from Shared.certoraLogging import logging_setup

SETTINGS_FLAG = "--settings"
PATIENT_FLAG = "-patient"
GRAPH_DRAW_LIMIT = "-graphDrawLimit"
REG_TEST_FLAG = "-regressionTest"
REGRESSION_OUTPUT_FLAG = "-regressionOutputFile"
JSON_FLAG = "-json"
SOLC_FLAG = "--solc"
ANALYSIS_STATS_FLAG = "-statisticsJson"
diffTableHeaders = ["Test path", "Missing from actual results"]  # type: List[str]
errors = ""
violated = False
SUCCESS = green_text("succeeded")
FAIL = red_text("failed")
MISS = orange_text("test is not defined")
LEFT = "left"
CENTER = "center"
CERTORA_RUN_CMD = "certoraRun"

SCRIPT_NAME = Path(__file__).name

logger = logging.getLogger("reg_test")

GLOBAL_TIMEOUT = 600

"""


        Note: This script expects run.sh to run certoraRun,
        because it appends --settings automatically


"""


def sort_text_file(source_file_path: Path, sorted_filename: Path) -> bool:
    """sort the source_filename (required for comparison) and store the results in sorted_filename"""
    global errors
    p = subprocess.Popen(["sort", source_file_path], stdout=sorted_filename.open("w"))

    try:
        exitcode = p.wait(timeout=15)
        if exitcode < 0:
            errors += f'[{SCRIPT_NAME}]: Text files comparison failed - ' \
                      f'sort file {source_file_path} returned with {exitcode}.\n'
            return False
        return True
    except subprocess.TimeoutExpired:
        p.kill()
        errors += f'[{SCRIPT_NAME}]: Text files comparison failed - sort file {source_file_path} timeout.\n'
        return False


def blacklist_check(results_file_path: Path) -> bool:
    """
    Checks the regression file against a black list - if the terms appear in the file, it indicates an error occurred
    @param results_file_path the regression text file from the run
    @return: true if no blacklisted term appears in the regression file
    """
    global errors

    blacklist = ["Error building calltrace for violation of rule"]

    result = True
    with results_file_path.open() as results_file:
        for line in results_file:
            for blacklisted_term in blacklist:
                if blacklisted_term in line:
                    errors += f"the term '{blacklisted_term}' appears in regression file"
                    result = False

    return result


def compare_files(table: List[List[str]], results_file_path: Path, expected_file_path: Path) -> bool:
    """
    compare expected file with the output so that expected is contained (entirely) in the output
    @param table: differences table, its structure is defined by 'diffTableHeaders':
        expected results filename, the line that is missing from the output
    @param results_file_path:
    @param expected_file_path:
    @return:
    """
    global errors
    # sort the expected results file (required for comparison)
    sorted_expected_file_path = Path("expected_sorted.txt")
    if not sort_text_file(expected_file_path, sorted_expected_file_path):
        return False

    # sort the output file (required for comparison)
    sorted_results_file_path = Path("actual_sorted.txt")
    if not sort_text_file(results_file_path, sorted_results_file_path):
        return False

    # In the comm output, we also see the content of both files in columns, but the key is the indentation.
    # The rightmost column displays the content that is the same in both files — up to a point.
    # The other two columns show (leftmost) the content that is unique to the first file and
    # (middle) the content that is unique to the second file.
    # -2: suppress lines unique to the output file (column 2)
    # -3: suppress lines common to expected.txt and actual.txt (column3)
    #
    # The following command presents the lines from expected.txt that is missing from the actual output
    cmd = f"comm -23 {sorted_expected_file_path} {sorted_results_file_path}"
    # print(f"Diff cmd: {cmd}")

    try:
        with subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, universal_newlines=True) as proc:
            if proc.stdout:
                equal = True
                for line in iter(proc.stdout.readline, ""):
                    append_row(table, expected_file_path, line)
                    equal = False
            else:
                equal = False
    except FileNotFoundError as e:
        logger.error(f"Could not execute command {cmd} - {e.strerror}")
        # In windows, just fail the test (to allow debugging), in other systems, fail the whole suite
        if is_windows():
            equal = False
        else:
            sys.exit(1)

    delete_file(sorted_expected_file_path)
    delete_file(sorted_results_file_path)
    return equal


def delete_file(path: Path) -> bool:
    if path.is_file():
        try:
            path.unlink()
        except OSError as e:
            logger.error(f"{e.filename} - {e.strerror}.")
            return False
    return True


def result_to_string(succeeded: Optional[bool]) -> str:
    result = MISS

    if succeeded is not None:
        result = SUCCESS if succeeded else FAIL
    return result


def update_results(result_sum: Optional[List[List[str]]], curr_test_dir: Path, regression_succeeded: Optional[bool],
                   verification_succeeded: Optional[bool], analysis_succeeded: bool, start_time: int,
                   run_file_path: Path) -> None:
    """
    used for creating test summary table
    @param result_sum:
    @param curr_test_dir:
    @param regression_succeeded - indicator for regression test success
    @param verification_succeeded - indicator for verification test success
    @param analysis_succeeded - indicator for analysis test results
    @param start_time:
    @param run_file_path:
    @return:
    """
    if result_sum is None:  # was added because of type check
        result_sum = []

    reg_result = result_to_string(regression_succeeded)
    json_result = result_to_string(verification_succeeded)
    analysis_result = result_to_string(analysis_succeeded)
    append_row(result_sum, curr_test_dir, reg_result, json_result, analysis_result, str(int(time.time()) - start_time),
               str(run_file_path))


def print_result_msg(curr_test_dir: Path, succeeded: Optional[bool],
                     title: str = "Textual Comparison Result (expected.txt)") -> None:
    result_msg = f"[{SCRIPT_NAME}] {title}: {curr_test_dir} - "
    result_msg += result_to_string(succeeded)
    print(result_msg)


def export_junit(table: List[List[str]], dir_path: Path, result_details: Dict[str, List[str]]) -> None:
    test_cases = []
    for row in table:
        name, regression_result, verification_result, analysis_result, time, file = row
        #  build base run prefix by merging "run" as a run id, then cut it. Dirty trick.
        #  we should have kept the base id in row even if we don't want to print it in the table
        base_run_id = file.replace(build_run_id(name, "run"), "").replace(".sh", "")
        run_key = build_run_id(name, base_run_id)
        name = run_key.replace(f'{dir_path}/', "")
        # if we run from run.sh in a folder, the run key will contain a trailing '/', which is bad.
        if len(run_key) > 0 and run_key[-1] == "/":
            run_key = run_key[:-1]
        # name should also not contain a trailing '/' as it comes up in the classname when --include option is used
        if len(name) > 0 and name[-1] == "/":
            name = name[:-1]
        test_case = TestCase(run_key, name, elapsed_sec=int(time))
        is_failure = (regression_result != SUCCESS and regression_result != MISS) or \
                     (verification_result != SUCCESS and verification_result != MISS) or (analysis_result != SUCCESS)
        if is_failure:
            regression_result_string = re.sub(
                f'[{BASH_RED_COLOR}{BASH_GREEN_COLOR}{BASH_ORANGE_COLOR}{BASH_END_COLOR}]',
                '',
                regression_result)
            verification_result_string = re.sub(
                f'[{BASH_RED_COLOR}{BASH_GREEN_COLOR}{BASH_ORANGE_COLOR}{BASH_END_COLOR}]', '',
                verification_result)
            analysis_result_string = re.sub(f'[{BASH_RED_COLOR}{BASH_GREEN_COLOR}{BASH_ORANGE_COLOR}{BASH_END_COLOR}]',
                                            '',
                                            analysis_result)
            message = f"verification {verification_result_string}, regression {regression_result_string}, " \
                      f"analysis {analysis_result_string}"
            details = result_details.get(run_key, [])
            txt = '\n'.join(details) + ("\n" if len(details) > 0 else "")
            txt += "To recreate the exception locally, type the following:\n"
            txt += "cd EVMVerifier;\n"
            txt += f"python scripts/regTest.py Test/{name}"
            if len(row) >= 6:
                txt += f"\nThe exact command can be found in {file}"
            test_case.add_failure_info(message, output=txt)
            # testCase.add_error_info(message)
        if regression_result == MISS and verification_result == MISS:
            test_case.add_failure_info(message="both verification and regression tests were not defined")
        test_cases.append(test_case)
    test_suite = TestSuite("Certora Test Suite", test_cases)
    # print(TestSuite.to_xml_string([testSuite])
    test_results_path = dir_path / 'certora.test.results.xml'
    with test_results_path.open('w+') as f:
        TestSuite.to_file(f, [test_suite], prettyprint=False)


def print_table(table: List[List[str]], headers: List[str], *align: Optional[str]) -> None:
    """
    print the differences table
    @param table:
    @param headers - define table headers
    @param align:
    inner@param tablefmt - table format (see https://pypi.org/project/tabulate/)
    inner@param colalign - column alignment
    @return:
    """
    if len(table) > 0:
        print(tabulate(table, headers, tablefmt="psql", colalign=(*align,)))


def append_row(table: List[List[str]], test_path: Path, *add_args: str) -> None:
    """
    add found violation to the differences table
    @param table - differences table
    @param test_path - test directory path
    @param addArgs - may be any other argument. For example:
    * lineIndex - line number in the expected file
    * lineContent - a line from the expected file which differ from the output
    """
    # was lineIndex: str, lineContent: str) -> None:
    table_row = [str(test_path)]

    for arg in add_args:
        table_row.append(arg)

    table.append(table_row)


def find_run_files(dir_path: Path) -> List[Path]:
    return sorted([run_file for run_file in Path(dir_path).glob("run*.sh")])


def get_output_file_path(curr_test_dir: Path) -> Path:
    """
    sets a name for regression output file by using current test directory
    @param curr_test_dir:current test directory
    @return: a name for regression output file
    """
    return Path(f'{curr_test_dir.name}Test.txt')


def get_optional_flag_value(cmd: str, flag: str) -> Optional[str]:
    """
    get an optional value that follows a flag in 'cmd'. A flag must be followed by either a space or a "=" sign.
    (we could do better parsing here :/ )
    @param cmd - command
    @param flag - flag name
    @return: the flag's value
    """
    try:
        flag_value = cmd[cmd.index(flag + " ") + len(flag) + 1:]
    except ValueError:
        try:
            flag_value = cmd[cmd.index(flag + "=") + len(flag) + 1:]
        except ValueError:
            return None

    # in case there are more flags pick the first one (flags are separated by ',')
    # before that, separate whitespaces too (separate between instances of settings)
    flag_value = flag_value.split(" ", 1)[0].split(",", 1)[0]
    return flag_value.strip('\"')  # remove wrapping quotes (if exist)


def get_flag_value(cmd: str, flag: str) -> str:
    """
    get a value that follows a flag in 'cmd'
    @param cmd - command
    @param flag - flag name
    @return:
    """
    res = get_optional_flag_value(cmd, flag)
    if res is None:
        logger.fatal(f"Flag {flag} not found in in command {cmd}")
        sys.exit(3)
    return res


def assign_reg_out_flag(regression_output_file: Path) -> str:
    """
    create key-value string with the regression output file flag and its value
    @param regression_output_file:
    @return: a key-value string with the regression output file flag and its value
    """
    return f'{REGRESSION_OUTPUT_FLAG}="{regression_output_file}"'


def execute_test(cmd: str, curr_test_dir: Path) -> bool:
    """
    run test by executing the supplied command (usually certoraRun with additional flags)
    @param cmd: The run command line of the test
    @param curr_test_dir: The directory where the test should be run at
    @returns false if the command execution failed, true if the command execution succeeded
    """
    success = False
    if is_certora_run_cmd(cmd):
        last_workdir = Path.cwd()
        pwd_replacement = (last_workdir / curr_test_dir).as_posix()
        expanded_cmd = cmd.replace("$PWD", pwd_replacement).replace("${PWD}", pwd_replacement)
        args = shlex.split(expanded_cmd)
        print("Running " + ' '.join(args))
        sys.stdout.flush()

        with change_working_directory(curr_test_dir):
            try:
                run_certora(args[1:], True)
                success = True
            except Exception as e:
                logger.error(f"Test failed: {e}", exc_info=e)
    else:
        certora_root_dir = as_posix(get_certora_root_directory())
        cmd = cmd.replace("$CERTORA", certora_root_dir)
        args = prepare_call_args(cmd)
        sys.stdout.flush()
        return_code = subprocess.call(args, shell=False,
                                      universal_newlines=True, cwd=curr_test_dir)

        if return_code != 0:
            logger.warning(f"return code -{return_code}")

        success = return_code == 0

    return success


def error_missing_file(curr_test_dir: Path, missing_file: Path) -> None:
    global errors
    errors += f'TEST ERROR: {curr_test_dir}. File {missing_file} does not exist.\n'


def get_expected_file_path(curr_test_dir: Path, file_to_look_for: Path) -> Optional[Path]:
    """
    Get expected artifact file path if it exists, else None
    @param curr_test_dir - full/relative directory path
    @param file_to_look_for - test artifact file name
    """
    file_path = curr_test_dir / file_to_look_for
    if file_path.exists():
        return file_path
    return None


def get_files_paths(curr_test_dir: Path, output_file: Path, expected_file: Path = Path("expected.txt")) \
        -> Tuple[Optional[Path], Optional[Path]]:
    """
    Get the expected file path and the regression output file path, if they exist. Otherwise, None is returned.
    @param curr_test_dir - full/relative directory path
    @param output_file - test output file name
    @param expected_file - expected output file name
    """
    expected_file_path = curr_test_dir / expected_file
    actual_file_path = curr_test_dir / output_file

    actual_file_exists = actual_file_path.exists()
    expected_file_exists = expected_file_path.exists()

    if actual_file_exists and expected_file_exists:
        return actual_file_path, expected_file_path

    if expected_file_exists:
        # Print error only when there is expected file
        # but the output is missing
        error_missing_file(curr_test_dir, actual_file_path)
        return None, expected_file_path
    return None, None  # both files are missing


def is_certora_run_cmd(cmd: str) -> bool:
    return cmd.lstrip().startswith(CERTORA_RUN_CMD)  # ignore leading space, then verify the first word is certoraRun


def add_flags_to_cmd(cmd: str, curr_test_dir: Path) -> str:
    """
    adds necessary flags to cmd (command)
    @param cmd: command
    @param curr_test_dir: path to current test directory
    @return: A new, modified command
    """
    global GLOBAL_TIMEOUT
    cmd = cmd.rstrip()
    if is_certora_run_cmd(cmd):
        added_settings = []
        if REG_TEST_FLAG not in cmd:  # regressionTest flag is missing
            added_settings.append(REG_TEST_FLAG)

        if REGRESSION_OUTPUT_FLAG not in cmd:  # regressionOutputFile flag is missing
            # set regression output file name
            reg_output_file = get_output_file_path(curr_test_dir)
            added_settings.append(assign_reg_out_flag(reg_output_file))

        if JSON_FLAG not in cmd:
            added_settings.append(f"{JSON_FLAG}=out.json")

        if ANALYSIS_STATS_FLAG not in cmd:
            added_settings.append(f"{ANALYSIS_STATS_FLAG}=analysis")

        if PATIENT_FLAG not in cmd:
            added_settings.append(f"{PATIENT_FLAG}=0")
        #    if graphDrawLimit not in cmd:
        #        added_settings.append(f"{graphDrawLimit}=0")

        #    added_settings.append("-lowFootprint=true")
        #    added_settings.append("-disablePopup=true")
        test_timeout_match = re.search(r"-globalTimeout=(\d+)", cmd)
        if test_timeout_match:  # A timeout was set for this test
            test_timeout = test_timeout_match[1]  # The timeout numeric value as a string
            if int(test_timeout) > GLOBAL_TIMEOUT:
                logger.warning(
                    f"timeout of the specified script, {test_timeout}, is greater than global "
                    f"maximal timeout of {GLOBAL_TIMEOUT}. Using the global maximal timeout instead."
                )
                re.sub(r'-globalTimeOut=\d+', f"-globalTimeout={GLOBAL_TIMEOUT}", cmd)  # replace the illegal timeout
        else:  # No timeout was set
            added_settings.append(f"-globalTimeout={GLOBAL_TIMEOUT}")
        added_settings.append("-verifyCache")
        added_settings.append("-verifyTACDumps")
        added_settings.append("-testMode")

        if added_settings:
            cmd += f" {SETTINGS_FLAG} {','.join(added_settings)}"

        cmd += " --disable_auto_cache_key_gen"
        cmd += " --javaArgs '\"-ea\"'"

    return cmd


def build_run_id(containing_dir_name: str, id: str) -> str:
    """
    From a given directory path (that may or may not end with a '/'),
    and a run id (the part after "run"), create a unique run/test identifier.

    @param containing_dir_name - directory containing the test
    @param id - the id of the test
    """
    if len(containing_dir_name) == 0:
        return id

    return f'{Path(containing_dir_name) / id}'


def check_stats_file_analysis(curr_test_dir: Path, run_file_id: str, analysis_json_file: Path,
                              solc: Optional[str], result_details: Dict[str, List[str]]) -> bool:
    global errors

    # skip old solidity versions 4 and 5?
    # if solc.startswith("solc4") or solc.startswith("solc5"):
    #    return True

    ret = True
    with analysis_json_file.open() as results_file:
        results = json.load(results_file)

    # this function assumes analysis_json_file exists
    analysis_key = "ANALYSIS"

    if analysis_key not in results:
        errors += f"TEST ERROR: {curr_test_dir}. There is no analysis entry in {analysis_json_file}\n"
        return False

    # we allow for an optional specific expected results expected{run_file_id}.analysis which is a json file
    expected_file_path = curr_test_dir / f"expected{run_file_id}.analysis"
    expected_file_exists = expected_file_path.exists()
    expected = {}
    if expected_file_exists:
        with expected_file_path.open() as expected_file:
            expected = json.load(expected_file)

    # global code prefixes to ignore
    excluded_codes_prefixes = ["constructor(", "ecrecover", "constructor_", "0"]  # the heck is 0?

    # pre compute a solc message
    if solc is not None:
        solc_message = f", compiled with {solc}"
    else:
        solc_message = ", compiled with default solc in executing machine"

    def check_analysis_for_code_with_expected(code: str, result: Any,
                                              expected_analysis_results: Dict[str, str],
                                              analysis: str) -> bool:
        global errors
        skip = False
        ret = True
        for prefix in excluded_codes_prefixes:
            if code.startswith(prefix):
                skip = True
                break
        if skip:
            return True

        msg = None
        expected_result = expected_analysis_results.get(code, None)
        if (expected_result is not None and not result and expected_result) or \
                (expected_result is None and not result):
            msg = f"Analysis {analysis} failed for {code} in {curr_test_dir}, test \"{run_file_id}\"{solc_message}"
        elif expected_result is not None and expected_result != result:
            msg = f"Analysis {analysis} expected result for {code} in {curr_test_dir}, test \"{run_file_id}\" " \
                  f"was {expected_result} but got {result}"

        if msg is not None:
            full_run_id = build_run_id(str(curr_test_dir), run_file_id)
            if full_run_id in result_details:
                result_details[full_run_id].append(msg)
            else:
                result_details[full_run_id] = [msg]
            errors += f"{msg}\n"
            ret = False

        return ret

    for analysis, code_names_to_results in results[analysis_key].items():
        expected_analysis_results = expected.get(analysis, {})
        # check all keys, with the exception of excluded prefixes of code names
        for subkey1, result_or_nested in code_names_to_results.items():
            if result_or_nested is Dict:
                for subkey2, maybe_result in result_or_nested.items():
                    if maybe_result is None:
                        errors += f"Got unexpected nested result for {subkey1}, {subkey2}: {maybe_result}\n"
                        ret = False
                        continue
                    expected_result_ = expected_analysis_results.get(subkey1, {})
                    ret = check_analysis_for_code_with_expected(subkey2, maybe_result, expected_result_,
                                                                analysis) and ret
            elif result_or_nested is not None:
                ret = check_analysis_for_code_with_expected(subkey1, result_or_nested,
                                                            expected_analysis_results, analysis) and ret
            else:
                errors += f"Got unexpected result for {subkey1}: {result_or_nested}\n"
                ret = False

    return ret


def verification_compare(curr_test_dir: Path, test_id: str, act_json_file: Path, exp_json_file: Path,
                         result_details: Dict[str, List[str]]) -> bool:
    global errors

    with act_json_file.open() as actual_file:
        actual = json.load(actual_file)
    try:
        with exp_json_file.open() as expected_file:
            expected = json.load(expected_file)
    except ValueError as E:
        errors += f"TEST ERROR: {curr_test_dir}. Could not read {exp_json_file}\n{E}"
        expected = {}

    if "rules" in actual and "rules" in expected:
        expected_assert_messages = {}
        if "assertMessages" in expected:
            expected_assert_messages = expected["assertMessages"]

        if expected_assert_messages and "assertMessages" not in actual:
            errors += f"TEST ERROR: {curr_test_dir}. Expected 'assertMessages',\
                       missing from the output file ({act_json_file})"
            verification_succeeded = False
        else:
            details = []  # type: List[str]
            test_name = str(curr_test_dir)
            verification_succeeded = \
                compare_results_with_expected(test_name, actual["rules"], expected["rules"],
                                              actual["assertMessages"], expected_assert_messages, True, details)
            test_key = build_run_id(str(curr_test_dir), test_id)
            if test_key in result_details:
                result_details[test_key] += details
            else:
                result_details[test_key] = details
    elif "tacResult" in actual and "tacResult" in expected:
        expected_result = expected["tacResult"]
        actual_result = actual["tacResult"]
        verification_succeeded = expected_result == actual_result
    else:
        verification_succeeded = False
    return verification_succeeded


def get_run_file_id(run_file_path: Path) -> str:
    _, run_file_id = run_file_path.stem.split("run", 1)
    return run_file_id


def is_long(run_file_id: str, path: Path) -> bool:
    """
    To ignore a run file, we `touch longRUNID` and commit the file.
    If the ignore file exists, reg test script will ignore it (unless long runs are explicitly requested, e.g. nightly)
    @param run_file_id: the id of the run (the part after 'run' and before '.sh')
    @param path: base path to the tests
    @return: if it should be a long run that is not run as part of the usual reg test
    """
    long_file = path / f"long{run_file_id}"
    return long_file.is_file()


def is_quick(run_file_id: str, path: Path) -> bool:
    """
    Marks a run script ID that if is marked as quick, it'll run in quick mode as well as in the usual mode.
    Quick mode is only for local runs that should be quicker than CI.
    Quick mode scripts are also running in the main CI run.
    @param run_file_id: the id of the run (the part after 'run' and before '.sh')
    @param path: base path to the tests
    @return: if it should be a quick run that is not run as part of the usual reg test
    """
    quick_file = path / f"quick{run_file_id}"
    return quick_file.is_file()


def is_ignored_path(path: Path) -> bool:
    ignore_file = path / "ignore.all"
    return ignore_file.is_file()


def is_ignored_analysis_path(run_file_id: str, path: Path) -> bool:
    ignore_analysis_file = path / f"ignoreAnalysis{run_file_id}"
    return ignore_analysis_file.is_file()


def regression_test(diff_table: List[List[str]], run_file_path: Path, curr_test_path: Optional[Path],
                    recursive: bool, result_sum: List[List[str]], long: bool, quick: bool,
                    result_details: Dict[str, List[str]]) -> None:
    """
    run regression test
    @param diff_table - differences table
    @param run_file_path - current run{}.sh file path
    @param curr_test_path - full/relative test path
    @param result_sum - test results summary table
    @param long
    @param quick
    @param recursive
    @param result_details - details about failures of specific tests
    """
    global violated
    run_file_id = get_run_file_id(run_file_path)
    if curr_test_path is not None:
        if is_long(run_file_id, curr_test_path) and not long:
            print(f"Ignoring long test {run_file_id} in {curr_test_path}")
            return None

        if not is_quick(run_file_id, curr_test_path) and quick:
            print(f"Ignoring non-quick test {run_file_id} in {curr_test_path} as we're in quick mode")
            return None

        if is_ignored_path(curr_test_path):
            print(f"Ignoring all tests in {curr_test_path}")
            return None

    info_str = "Starting test"
    if run_file_id != "":
        info_str += f" {run_file_id}"
    if curr_test_path is not None:
        info_str += f" in {curr_test_path}"
    print(info_str)

    start_time = int(time.time())

    reg_succeeded = ver_succeeded = True  # type: Optional[bool]
    analysis_succeeded = True

    # read run.sh
    run_cmd = ""
    with run_file_path.open() as f:
        for line in f.read().splitlines():
            line = line.split("#")[0]  # Ignore bash comments
            if line.endswith('\\'):    # in case the bash command was split to a few different lines using \
                line = line[0:-1]
            line = line.strip()        # Remove tabs in the beginning of the line and excess spaces
            run_cmd += line + " "      # Adding a space as a safety measure, so no words will be combined

    if curr_test_path is None:
        curr_test_path = run_file_path.parent.resolve()
        # update command if necessary

    run_cmd = add_flags_to_cmd(run_cmd, curr_test_path)

    print(f"command: {run_cmd}")

    if is_certora_run_cmd(run_cmd):
        # get regression output file name
        reg_output_file = Path(get_flag_value(run_cmd, REGRESSION_OUTPUT_FLAG))
        # get verification output file name
        ver_output_file = Path(get_flag_value(run_cmd, JSON_FLAG))
        # get analysis output file name
        analysis_output_file = Path(f"{get_flag_value(run_cmd, ANALYSIS_STATS_FLAG)}.json")

        # remove previous regression results
        reg_is_deleted = delete_file(curr_test_path / reg_output_file)
        # remove previous verification results
        ver_is_deleted = delete_file(curr_test_path / ver_output_file)
        # remove previous analysis results
        analysis_is_deleted = delete_file(curr_test_path / analysis_output_file)

        if not reg_is_deleted:
            reg_succeeded = False
            print_result_msg(curr_test_path, reg_succeeded, f"Textual Comparison Result (expected{run_file_id}.txt)")

        if not ver_is_deleted:
            ver_succeeded = False
            print_result_msg(curr_test_path, ver_succeeded, f"Verification Result (expected{run_file_id}.json)")

        if not analysis_is_deleted:
            analysis_succeeded = False
            print_result_msg(curr_test_path, analysis_succeeded,
                             f"Analysis Result (optional expected{run_file_id}.analysis)")

        # if no expected file was found, print failed and return
        if not reg_succeeded and not ver_succeeded:
            violated = True
            update_results(result_sum, curr_test_path, reg_succeeded, ver_succeeded, analysis_succeeded,
                           start_time, run_file_path)
            return None

        execute_test(run_cmd, curr_test_path)

        # get reg files paths
        expected_reg_path = Path(f"expected{run_file_id}.txt")
        act_reg_file, exp_reg_file = get_files_paths(curr_test_path, reg_output_file, expected_reg_path)

        # get verification files paths (TODO: Why not json flag's value i.e. ver_output_file?)
        verification_out_path = Path("out.json")
        expected_verification_path = Path(f"expected{run_file_id}.json")
        act_json_file, exp_json_file = get_files_paths(curr_test_path, verification_out_path,
                                                       expected_verification_path)

        # get analysis file path
        act_analysis_file = get_expected_file_path(curr_test_path, analysis_output_file)

        #  VERIFICATION
        if exp_json_file:  # if expected.json found
            if not ver_is_deleted or not act_json_file:
                # if we couldn't delete prev results
                # or there is no output file
                ver_succeeded = False
            else:
                ver_succeeded = \
                    verification_compare(curr_test_path, run_file_id, act_json_file, exp_json_file, result_details)
        else:
            ver_succeeded = None
        print_result_msg(curr_test_path, ver_succeeded, f"Verification Result (expected{run_file_id}.json)")

        #  REGRESSION
        if act_reg_file is not None:
            blacklist_check_res = blacklist_check(act_reg_file)
        else:
            blacklist_check_res = True

        if exp_reg_file is not None:  # if expected.txt found
            if not reg_is_deleted or act_reg_file is None:  # if there is no output or we couldn't delete prev results
                reg_succeeded = False
            else:
                reg_succeeded = compare_files(diff_table, act_reg_file, exp_reg_file)
                reg_succeeded = reg_succeeded and blacklist_check_res
        else:
            reg_succeeded = blacklist_check_res
        print_result_msg(curr_test_path, reg_succeeded, f"Textual Comparison Result (expected{run_file_id}.txt)")

        #  ANALYSIS
        do_analysis_test = not is_ignored_analysis_path(run_file_id, curr_test_path)
        if act_analysis_file is not None and do_analysis_test:
            solc_flag = get_optional_flag_value(run_cmd, SOLC_FLAG)
            analysis_succeeded = \
                check_stats_file_analysis(curr_test_path, run_file_id, act_analysis_file, solc_flag, result_details)
        elif act_analysis_file is None and do_analysis_test:
            logger.warning(
                f"No analysis result for {run_file_id} despite requesting it. "
                f"It may be better to ignore analysis results by adding the file "
                f"\"ignoreAnalysis{run_file_id}\"")
            analysis_succeeded = False
        else:
            analysis_succeeded = True
        print_result_msg(curr_test_path, analysis_succeeded, "Analysis Result")

        if not violated:
            # violated == True <=> one of the tests has failed
            violated = (reg_succeeded is not None and not reg_succeeded) or \
                       (ver_succeeded is not None and not ver_succeeded) or \
                       (not analysis_succeeded) or \
                       (reg_succeeded is None and ver_succeeded is None)
    else:
        ver_succeeded = execute_test(run_cmd, curr_test_path)
        reg_succeeded = None
        print_result_msg(curr_test_path, ver_succeeded, "Execution result (exitcode 0 to succeed)")
        if not violated:
            violated = not ver_succeeded

    if recursive:
        update_results(result_sum, curr_test_path, reg_succeeded, ver_succeeded, analysis_succeeded, start_time,
                       run_file_path)


def prepare_for_reg_test(curr_test_path: Path, diff_table: List[List[str]], result_sum: List[List[str]],
                         recursive: bool, long: bool, quick: bool, result_details: Dict[str, List[str]]) -> None:
    """
    @param curr_test_path - full/relative directory/run*.sh file path
    @param diff_table - differences table
    @param result_sum - test results summary table
    @param recursive
    @param long
    @param quick
    @param result_details - optional dictionary for filling in failure details
    """
    global violated
    if curr_test_path.is_dir():
        # find all run*.sh files
        run_files = find_run_files(curr_test_path)
        if len(run_files) == 0 and not recursive:  # specific directory test
            # in recursive mode, when run.sh is not found (in 'currTestDir' folder)
            # we skip this folder and go to the next one.
            # there will be NO ERROR message
            print_result_msg(curr_test_path, False)
            print_result_msg(curr_test_path, False, "Verification Result (expected.json)")
            violated = True
            return None
        for runFile in run_files:
            print(f"Visiting {curr_test_path}")
            regression_test(diff_table, runFile, curr_test_path, recursive, result_sum, long, quick,
                            result_details)
    elif curr_test_path.is_file():
        regression_test(diff_table, curr_test_path, None, False, result_sum, long, quick, result_details)


def exclude_filter(dir_name: str, ignore_dirs: Optional[str]) -> bool:
    """
    check if directory name starts with a dot or 'emv' (which are usually prev tests output)
    we can explicitly pass any dir name we want to ignore
    @param dir_name:
    @param ignore_dirs:
    @return:
    """
    ignore_list = ignore_dirs.split(",") if ignore_dirs else []

    if dir_name.startswith((".", "emv-")) or dir_name in ignore_list:
        return True
    return False


def print_usage() -> None:
    print("""Usage: DIR_NAME [options...]
       [--recursive]
       [--include SUB_DIR_NAME1,SUB_DIR_NAME2] (will disable --ignore and --recursive)
       [--ignore SUB_DIR_NAME1,SUB_DIR_NAME2,...]

       Output:
       Verification Result - compares rules results with those from expected.json
       Textual Comparison Result - checks if all the lines from expected.txt appear in the textual output
       """,
          flush=True)


@click.command()
@click.argument("path")
@click.option("--recursive", is_flag=True, help="run recursively on PATH")
@click.option("--include", type=click.STRING, help="subdirectories separated by ',' (no space). "
                                                   "Run regression test on the supplied subdirectories")
@click.option("--ignore", type=click.STRING, help="subdirectories separated by ',' (no space). "
                                                  "Used along with --recursive")
@click.option("--long", is_flag=True, help="include long tests")
@click.option("--quick", is_flag=True, help="run only quick tests")
@click.option("--global_timeout", type=click.INT, help="globalTimeout value", default=600, show_default=True)
def main(path: str, recursive: Optional[bool], include: Optional[str], ignore: Optional[str],
         long: bool, quick: bool, global_timeout: int) -> None:
    """Run regression test on PATH by looking for run*.sh files

    Can be executed on:
    - specific run file/directory
    - a few subdirectories (by supplying a parent directory as PATH and
      using --include)
    - directory tree (by supplying a directory path as PATH and using --recursive.
      --ignore can be used for skipping first level sub directory/ies)

    Output:

    Verification Result - compares rules results with those from expected.json
    Textual Comparison Result - checks if all the lines from expected.txt appear in the textual output from our
    specialized regression logger (Logger.regression())"""
    global errors
    global GLOBAL_TIMEOUT
    GLOBAL_TIMEOUT = global_timeout  # yikes
    result_sum = []  # type: List[List[str]]
    diff_table = []  # type: List[List[str]]
    headers = ["Test", "Regression", "Verification", "Analysis", "Time", "Run file"]

    if long and quick:
        logger.fatal("Cannot run in both long and quick modes")
        sys.exit(1)

    _path = Path(path)

    result_details = {}  # type: Dict[str, List[str]]
    if recursive:
        if not _path.is_dir():
            logger.fatal(
                "Error occurred when traversing a directory. Please supply a directory when using recursive option\n")
            sys.exit(1)

        prepare_for_reg_test(_path, diff_table, result_sum, True, long, quick, result_details)

        # traverse all subdirectories inside 'dirPath'
        for curr_path in Path(_path).rglob("*"):
            if curr_path.is_dir() and not exclude_filter(curr_path.name, ignore):
                prepare_for_reg_test(curr_path, diff_table, result_sum, True, long, quick, result_details)

        print("Test Summary")
        print_table(result_sum, headers, LEFT, CENTER, CENTER, CENTER, CENTER, LEFT)
        export_junit(result_sum, _path, result_details)
    elif include:
        # Will recurse on subdirectories within the included directories
        if not _path.is_dir():
            logger.fatal("Please supply a directory when using include option\n")
            sys.exit(1)
        include_dirs = include.split(",")
        print(f"Running on directories {include_dirs}")
        for directory in include_dirs:
            if directory != "":
                """
                There are some slight differences between "./dir" and "dir"
                as far as prepare_for_reg_test is handling things.
                We want just "dir", if given directory is ".".
                See notional/notionalMatchAsStorageHash in customers code
                """

                """
                User runs in current directory.
                If user wants to run in `dir`, they should supply `dir` and not "./dir",
                but we are not checking that here.
                """
                if path != ".":
                    full_dir = _path / directory
                else:
                    full_dir = Path(directory)

                # We do a little 'trick': as 'global' in CircleCI doesn't split well directory names with spaces,
                # we replaced them with triple underscores. Here, we replace them back to a space
                full_dir = Path(str(full_dir).replace("___", " "))

                if not full_dir.is_dir():
                    logger.fatal(f"Invalid directory {full_dir} relative from {Path.cwd()}\n")
                    sys.exit(1)
                prepare_for_reg_test(full_dir, diff_table, result_sum, recursive=True, long=long, quick=quick,
                                     result_details=result_details)

        print_table(result_sum, headers, LEFT, CENTER, CENTER, CENTER, CENTER)
        export_junit(result_sum, _path, result_details)
    else:
        prepare_for_reg_test(_path, diff_table, result_sum=[], recursive=False, long=long, quick=quick,
                             result_details={})

    if diff_table:
        print()
        print("Textual Comparison Result:")
        print_table(diff_table, diffTableHeaders, LEFT, CENTER)
        print()

    get_violations()

    errors += get_errors()
    if errors:
        logger.error("Verification errors:")
        print(errors)

    if violated:  # indicates an error occurred
        sys.exit(1)


if __name__ == "__main__":
    logging_setup()
    main()
