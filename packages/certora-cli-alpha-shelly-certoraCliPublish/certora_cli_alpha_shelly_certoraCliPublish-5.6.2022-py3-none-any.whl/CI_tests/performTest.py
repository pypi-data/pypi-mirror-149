#!/usr/bin/env python3

import click
import os
import psycopg2  # type: ignore
import statistics
import sys
import pathlib
from typing import Any, List

scripts_dir_path = pathlib.Path(__file__).parent.parent.resolve()  # one directory up
sys.path.insert(0, str(scripts_dir_path))
from Shared.certoraUtils import get_readable_time
from Shared.certoraLogging import logging_setup
import logging

logging_setup()

test_logger = logging.getLogger("performance")


def values_mean(lst: List[float]) -> float:
    return statistics.mean(lst)


def execute(query: str) -> List[Any]:
    endpoint = os.environ.get("AWS_ENDPOINT", "")
    port = os.environ.get("AWS_PORT", 0)
    dbname = os.environ.get("AWS_DBNAME", "")
    user = os.environ.get("AWS_DB_USER", "")
    pwd = os.environ.get("AWS_DB_PWD", "")

    try:
        conn = psycopg2.connect(host=endpoint, port=port, database=dbname, user=user, password=pwd)
        cur = conn.cursor()

        cur.execute(query)
        query_result = cur.fetchall()
        print(query_result)
        # Make the changes to the database persistent
        conn.commit()
        # Close communication with the database
        cur.close()
        conn.close()
        return query_result
    except psycopg2.Error as e:
        print(f"Database connection failed due to {e.pgerror}")
        sys.exit(1)


def performance_check(pipeline: str, job_name: str, num: int, threshold: float, branch: str) -> bool:
    """
    Compares current test overall runtime with {num} previous tests average
    """
    sql = "SELECT ci_job_id, SUM(overall_runtime_milliseconds), git_branch, ci_build_nr " \
          "FROM ci_job_to_tool_runs " \
          "JOIN tool_runs ON tool_runs.id = ci_job_to_tool_runs.tool_run_id " \
          "JOIN (SELECT git_branch, ci_job_id as ci_id, ci_build_nr FROM ci_jobs) ci_jobs_alias " \
          "ON ci_jobs_alias.ci_id = ci_job_to_tool_runs.ci_job_id " \
          f"WHERE outputs_s3_bucket like '%/{job_name}/%' and ci_build_nr <= {pipeline} " \
          "GROUP BY ci_job_id, ci_build_nr, git_branch "
    if branch:
        sql += f"HAVING git_branch = '{branch}' "
    sql += f"ORDER BY ci_build_nr DESC NULLS LAST LIMIT {num + 1}"
    # NULLS FIRST|LAST explained: By default, NULL values are sorted and ranked first in DESC ordering
    current_result = execute(sql)

    if current_result is None:
        return False

    results = []
    for row in current_result:
        result = {"ci_job_id": row[0],
                  "sum": row[1],
                  "git_branch": row[2],
                  "ci_build_nr": row[3]}
        results.append(result)
    print(results)
    # result syntax:
    # [{"ci_build_nr": 1234, "sum": 321, "git_branch": 'master', "ci_job_id": '1234_smart_reg_test'},...]

    try:
        # First element is the most recent test results
        if results[0]['ci_build_nr'] != pipeline:
            test_logger.error("Couldn't get last test results")
            return False
    except IndexError:
        test_logger.error("couldn't find matching records.")
        return False

    current_overall_time = results[0]['sum']
    duration = get_readable_time(int(current_overall_time))
    print(f"current test overall time: {duration} ({current_overall_time}ms)")

    previous_results = [i.get("sum", 0) if i.get("sum", 0) is not None else 0 for i in results[1:]]
    if len(previous_results) < 1:  # shouldn't fail as it's the first CI test on current branch
        test_logger.warning("current test succeeded as no previous test was found")
        return True

    previous_avg = values_mean(previous_results)
    duration = get_readable_time(int(previous_avg))
    print(f"previous {len(previous_results)} test/s average time: {duration} ({previous_avg}ms)")

    # current overall_time - previous average overall_time
    gap = current_overall_time - previous_avg
    fraction = gap / previous_avg
    if fraction > 0:
        print(f"Current test resulted in increase of {round(fraction * 100, 2)} percent")
        if fraction > threshold:
            print("Current test failed")
            return False
    elif fraction < 0:
        print(f"Current test resulted in decrease of {round(abs(fraction) * 100, 2)} percent")
    else:
        print("Current test overall time equals to 5 previous tests average")
    return True


@click.command()
@click.option('-pipe', '--pipeline', required=True, type=int, help='pipeline num')
@click.option('-job', '--job-name', required=True, help='circleci job')
@click.option('-n', '--num', default=5, help='max number of circle_jobs used for calculations')
@click.option('-thr', '--threshold', default=0.3, help='max allowed gap between the current test and previous result')
@click.option('-b', '--branch', required=True, help='Branch')
def main(pipeline: str, job_name: str, num: int, threshold: float, branch: str) -> None:
    """
    find stats matching pipeline and job_name in db and perform some calculations
    """

    is_success = performance_check(pipeline, job_name, num, threshold, branch)
    if not is_success:
        sys.exit(1)


if __name__ == "__main__":
    main()
