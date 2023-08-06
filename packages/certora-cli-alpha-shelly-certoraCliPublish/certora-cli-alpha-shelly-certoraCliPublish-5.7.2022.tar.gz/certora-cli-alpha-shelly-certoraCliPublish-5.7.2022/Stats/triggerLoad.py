#!/usr/bin/env python3

import boto3
import click
import multiprocessing
import os
import psycopg2  # type: ignore
import sys

from typing import List, Tuple


def execute(query: str) -> int:
    endpoint = os.environ.get("AWS_ENDPOINT", "")
    port = os.environ.get("AWS_PORT", 0)
    dbname = os.environ.get("AWS_DBNAME", "")
    user = os.environ.get("AWS_DB_USER", "")
    pwd = os.environ.get("AWS_DB_PWD", "")

    try:
        conn = psycopg2.connect(host=endpoint, port=port, database=dbname, user=user, password=pwd)
        cur = conn.cursor()
        cur.execute(query)
        query_results = cur.fetchall()
        print(query_results)
        # Make the changes to the database persistent
        conn.commit()
        # Close communication with the database
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Database connection failed due to {e.pgerror}")
        print(f"Database error code - {e.pgcode}")
        return 1
    return 0


def load_data(sql_queries: List[str]) -> None:
    pool_size = min(multiprocessing.cpu_count(), 4)  # CircleCI declares 2, but detection reads 36
    with multiprocessing.Pool(pool_size) as pool:
        # chops the sql_queries into a number of chunks and submits to the process pool as separate tasks
        result = pool.map(execute, sql_queries, 2)

    if sum(result) > 0:
        # there was an error
        sys.exit(1)


def get_header(bucket: str, file_path: str) -> str:
    session = boto3.session.Session(
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_DEV'],
        aws_secret_access_key=os.environ['AWS_SECRET_KEY_DEV'],
        region_name=os.environ['AWS_REGION']
    )
    s3 = session.resource('s3')
    f = s3.Object(bucket, file_path)
    try:
        response = f.get()
        if 'Body' in response:
            streaming_body = response['Body']
            it = streaming_body.iter_lines()
            first_line = next(it)
            header = first_line.decode()
            return header
        else:
            print("S3 response object does not include 'Body' attribute")
    except Exception as e:
        print("Error occurred:", str(e))
    return ''


def prepare_query(bucket: str, region: str, table_name: str, job_name: str, pipeline: int, c: int = None) -> str:
    """
    Creates a query to get a csv file from S3 and insert all its content to the required table
    Returns an empty string if the csv file was not found (or couldn't be read)

    Query structure:
    "SELECT aws_s3.table_import_from_s3('{table_name}',
                                        '{column_list:csv file header}',
                                        '{options}',
                                        '{bucket}',
                                        '{file path}',
                                        'AWS_REGION')"
    For example:
    "SELECT aws_s3.table_import_from_s3('ci_job_to_tool_runs',
                                        'ci_job_id,tool_run_id',
                                        '(format csv,HEADER true)',
                                        'certora-ci',
                                        '10894/smart_reg_test/ci_job_to_tool_runs_0.csv',
                                        {AWS_REGION})"
    """
    query = f"SELECT aws_s3.table_import_from_s3('{table_name}', "
    file_path = f"{pipeline}/{job_name}/{table_name}"
    if c is not None:
        file_path += f"_{c}"
    file_path += ".csv"
    print(file_path)
    #
    header = get_header(bucket, file_path)
    if header:
        query += f"'{header}', '(format csv,HEADER true)', "
        query += f"'{bucket}', '{file_path}', '{region}')"
    else:
        return ''
    return query


@click.command()
@click.option('-b', '--bucket', required=False, default='certora-ci', help='bucket name')
@click.option('-pipe', '--pipeline', required=True, type=int, help='pipeline number')
@click.option('-job', '--job-name', required=True, help='circleci job name')
@click.option('-node', '--node-index', type=int, help='circle node index')
@click.argument('tables', nargs=-1)
def main(bucket: str, pipeline: int, job_name: str, node_index: int, tables: Tuple[str]) -> None:
    """Copy data from Storage to DB by looking for the TABLES_* files"""
    sql_queries = []

    region = os.environ['AWS_REGION']
    for table_name in tables:
        if node_index is not None and node_index >= 0:
            query = prepare_query(bucket, region, table_name, job_name, pipeline, node_index)
        else:
            query = prepare_query(bucket, region, table_name, job_name, pipeline)
        if query:  # ignore empty queries
            sql_queries.append(query)

    if len(sql_queries) > 0:
        print("Here are the queries:")
        print(sql_queries)
        load_data(sql_queries)
    else:
        print("Nothing to load. Make sure you added at least one table name")
        sys.exit(1)


if __name__ == "__main__":
    main()
