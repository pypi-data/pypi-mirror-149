import unittest
import os
import sys
from typing import Any
from pathlib import Path

scripts_dir_path = Path(__file__).parent.parent.resolve()  # one directory up
sys.path.insert(0, str(scripts_dir_path))
from EVMVerifier import certoraJobList
from Shared.certoraUtils import RECENT_JOBS_FILE
from Shared.certoraUtils import get_certora_root_directory


class TestRecentJobs(unittest.TestCase):
    @staticmethod
    def get_job_list_ob() -> Any:
        return certoraJobList.JobList()

    @staticmethod
    def get_job_list_file_path() -> Path:
        recent_jobs_path = Path(get_certora_root_directory()) / RECENT_JOBS_FILE
        return recent_jobs_path

    def test_missing_file(self) -> None:
        try:
            self.get_job_list_ob()
        except FileNotFoundError:
            self.fail("Missing recent jobs file throwing exception")

    def test_wrong_format(self) -> None:
        try:
            recent_jobs_path = self.get_job_list_file_path()
            with recent_jobs_path.open("w+") as f:
                f.write('{a:}')
            self.get_job_list_ob()
            self.assertFalse(os.path.exists(recent_jobs_path), "Incompatible file should be removed/renamed")
        except ValueError:
            self.fail("Wrong recent jobs file format throwing exception")

    def test_incompatible_file(self) -> None:
        try:
            recent_jobs_path = self.get_job_list_file_path()
            with recent_jobs_path.open("w+") as f:
                f.write('[{"path": "/", "job_id": "1234"}]')
            job_list = self.get_job_list_ob()
            job_id = "111"
            output_url = "https://output_url/"
            msg = "message"
            domain = "https://output_url/"
            user_id = "222"
            anonymous_key = "333"
            job_list.add_job(job_id, output_url, msg, domain, user_id, anonymous_key)
            self.assertFalse(os.path.exists(recent_jobs_path), "Incompatible file should be removed/renamed")
        except ValueError:
            self.fail("Wrong recent jobs file format throwing exception")

    def test_add_new_job(self) -> None:
        recent_jobs_path = self.get_job_list_file_path()
        with recent_jobs_path.open("w+") as f:
            f.write('{}')
        job_list = self.get_job_list_ob()
        job_id = "111"
        output_url = "https://output_url/"
        msg = "message"
        domain = "https://output_url/"
        user_id = "222"
        anonymous_key = "333"
        job_list.add_job(job_id, output_url, msg, domain, user_id, anonymous_key)
        job_list.save_data()
        with recent_jobs_path.open() as f:
            content = f.read()
            self.assertIn(job_id, content)
            self.assertIn(output_url, content)
            self.assertIn(msg, content)
