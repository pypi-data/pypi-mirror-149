import sys
import click
import os
from datetime import datetime
import logging
from pathlib import Path

scripts_dir_path = Path(__file__).parent.parent.resolve()  # one directory up
sys.path.insert(0, str(scripts_dir_path))
from Shared.certoraUtils import output_to_csv
from Stats.collectStats import upload_csv_files
from Shared.certoraLogging import logging_setup

logger = logging.getLogger("collections")


@click.command()
@click.option('-b', '--bucket', required=False, default='certora-ci', help='bucket name')
@click.option('-pipe', '--pipeline', required=True, type=int, help='pipeline number')
@click.option('-job', '--job-name', required=True, help='circleci job name')
@click.option('-table', '--table-name', required=True, help='circleci job name')
def main(bucket: str, pipeline: int, job_name: str, table_name: str) -> None:
    fieldnames = ['ci_build_nr', 'ci_job_id', 'ci_job_name', 'git_branch', 'git_hash', 'time_started']
    row = {
        'ci_build_nr': pipeline,
        'ci_job_id': f'{pipeline}_{job_name}',
        'ci_job_name': job_name,
        'git_branch': os.environ['CIRCLE_BRANCH'],
        'git_hash': os.environ['CIRCLE_SHA1'],
        'time_started': datetime.utcnow().isoformat()
    }

    if output_to_csv(table_name, fieldnames, row):
        upload_csv_files(bucket, pipeline, job_name, {table_name})
    else:
        logger.fatal(f"Couldn't create a csv file for {table_name}.")
        sys.exit(1)


if __name__ == '__main__':
    logging_setup()
    main()
