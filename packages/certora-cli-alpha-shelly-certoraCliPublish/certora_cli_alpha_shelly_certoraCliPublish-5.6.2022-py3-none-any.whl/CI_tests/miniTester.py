from typing import Any, Dict, List, Optional
from tabulate import tabulate
from Shared.certoraUtils import orange_text

errors = ""
warnings = ""
table = []  # type: List[List[str]]
violations_headers = ["Test name", "Rule", "Function", "Result", "Expected"]


def add_error(errors_str: str, test_name: str, rule: str, rule_result: str, expected_result: str = "",
              func_name: str = "") -> str:
    errors_str += f"Violation in {test_name}: {rule}"
    if func_name != "":
        errors_str += f", {func_name}"
    errors_str += f" result is {rule_result}."
    if expected_result != "":
        errors_str += f" Should be {expected_result}"
    errors_str += "\n"
    return errors_str


def print_table(headers: List[str]) -> None:
    print(tabulate(table, headers, tablefmt="psql"))


def find_expected(func_name: str, results_list: Dict[str, List[str]]) -> str:
    expected_result = orange_text("missing")
    for result in results_list.keys():
        if func_name in results_list[result]:
            expected_result = result
            break
    return expected_result


def append_violation(_table: List[List[str]], test_name: str, actual_result: str, expected_result: str,
                     rule_name: str = "", func_name: str = "") -> None:
    table_row = [test_name, rule_name, func_name, actual_result, expected_result]
    _table.append(table_row)


def compare_results_with_expected(
        test_name: str,
        rules_results: Dict[str, Any],
        expected_rules_results: Dict[str, Any],
        assert_messages: Dict[str, Any],
        expected_assertion_messages: Optional[Dict[str, Any]],
        test: bool,
        details: List[str]
) -> bool:
    """
    compare jar results with the expected results from file
    :param test_name: name of the test
    :param rules_results: a dictionary that includes all the rule names and their results from the jar output
    :param expected_rules_results: a dictionary that includes all the rule names and their results from tester file
    :param assert_messages: a dictionary that includes all the rule names and their assertion messages from the jar
           output
    :param expected_assertion_messages: a dictionary that includes all the rule names and their assertion messages from
           tester file
    :param test: a boolean indicator of current test (test==false <=> at least one error occurred
    :param details: details about failures
    :return: True if the two results are identical, False otherwise
    """
    global errors
    global warnings

    if rules_results != expected_rules_results:
        for rule in rules_results.keys():
            rule_result = rules_results[rule]
            if rule in expected_rules_results.keys():
                if isinstance(rule_result, str):  # flat rule ( rule_name: result )
                    if rule_result != expected_rules_results[rule]:
                        test = False
                        # errors = add_error(errors, testName, rule, rule_result, expected_rules_results[rule])
                        append_violation(table, test_name, rules_results[rule], expected_rules_results[rule], rule, "")
                        details.append(f"Unexpected result for rule {rule}")

                else:  # nested rule ( ruleName: {result1: [functions list], result2: [functions list] ... } )
                    for result, funcList in rule_result.items():
                        funcList.sort()
                        if isinstance(expected_rules_results[rule], str):
                            append_violation(table, test_name, result, "non parametric rule", rule, "")
                        else:
                            # maybe the rule status (e.g. SANITY_FAIL) is new and does not appear in the expected
                            # this is ok if the list of functions that match this result is empty
                            rule_result_exists_in_expected = result in expected_rules_results[rule]
                            if not rule_result_exists_in_expected and len(funcList) > 0:
                                append_violation(table, test_name, result, f"did not expect result {result} in {rule}",
                                                 rule, "")
                            elif rule_result_exists_in_expected:
                                expected_rules_results[rule][result].sort()

                                # compare functions sets (current results with expected)
                                if funcList != expected_rules_results[rule][result]:
                                    for funcName in funcList:
                                        # if function appears in current results but doesn't appear in the expected
                                        if funcName not in expected_rules_results[rule][result]:
                                            test = False
                                            # errors = add_error(errors, test_name, rule, result, "", func_name)
                                            expected_result = find_expected(funcName, expected_rules_results[rule])
                                            append_violation(table, test_name, result, expected_result, rule, funcName)
                                            details.append(f"Unexpected result for rule {rule} in {funcName}")
            else:
                test = False
                result = (rule_result
                          if isinstance(rule_result, str)
                          else "Object{" + ", ".join(rule_result.keys()) + "}")
                append_violation(table, test_name, result, orange_text("missing"), rule, "")
                details.append(f"Missing result for rule {rule}")
                # errors += f"{testName}, {rule} is not listed in 'rules'. Expected rules: " \
                #           f"{','.join(expectedRulesResults.keys())}\n"

    # if assertMessages field is defined (in tester)
    if expected_assertion_messages:
        for rule in expected_assertion_messages.keys():
            if rule not in assert_messages:  # current rule is missing from 'assertMessages' section in current results
                test = False
                details.append(f"Wrong assertion message in rule {rule}")

                errors += f'{test_name}, rule "{rule}"; ' \
                          f'expected: FAIL with assertion message "{expected_assertion_messages[rule]}"; ' \
                          f'observed: '

                if rule in rules_results.keys():  # rule is included in the output
                    errors += '<no assert message>\n'
                else:
                    errors += 'not found in the output\n'

            elif expected_assertion_messages[rule] != assert_messages[rule]:
                # assertion messages are different from each other
                test = False
                details.append(f"Wrong assertion message in rule {rule}")

                errors += f'{test_name}, rule "{rule}"; ' \
                          f'expected: FAIL with assertion message "{expected_assertion_messages[rule]}"; ' \
                          f'observed: FAIL with '
                if assert_messages[rule]:
                    errors += f'assertion message "{assert_messages[rule]}"\n'
                else:
                    errors += '<no assert message>\n'
    return test


def get_errors() -> str:
    return errors


def has_violations() -> bool:
    if table:
        return True
    else:
        return False


def get_violations() -> None:
    if table:
        print("Found violations:")
        print_table(violations_headers)
