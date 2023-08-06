import unittest
import subprocess
import os
import sys
from typing import List
from pathlib import Path
import atexit

scripts_dir_path = Path(__file__).parent.parent.resolve()  # one directory up
sys.path.insert(0, str(scripts_dir_path))
from Shared.certoraUtils import remove_file
import certoraRun


class TestVersionFlag(unittest.TestCase):
    """
    BEFORE RUNNING THE TEST: ensure that the version is in $VERSION
    by using export VERSION="1.0"
    """

    def test_correct_version(self) -> None:
        """
        BEFORE RUNNING THE TEST: ensure that the version is in $VERSION
        by using export VERSION="1.0"
        """
        version_str = os.environ['VERSION']
        self.assertEqual(certoraRun.get_version(), version_str, msg='version should be ' + version_str)

    @staticmethod
    def call_with_args(cli_args: List[str]) -> int:
        certora_run_path = scripts_dir_path / 'certoraRun.py'
        argv = [sys.executable, str(certora_run_path)] + cli_args + ['--check_args']

        if '--solc' not in argv:
            argv += ['--solc', 'solc6.10']
        res = subprocess.call(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # res = subprocess.call(argv)  # for DEBUG
        return res  # 0 is success

    def test_version(self) -> None:
        solidity_file = 'rome.sol'

        atexit.register(remove_file, solidity_file)

        with open(solidity_file, 'w') as f:
            f.write('')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--version']), msg='typical use case')
        self.assertEqual(0, self.call_with_args([solidity_file, '--assert', 'rome', '--version']),
                         msg='typical use of --version')

        self.assertEqual(0, self.call_with_args(['rome.sol', 'borborygmos', '--version']),
                         msg='We do not care for other errors in the command line if the --version flag is present')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--version', 'borborygmos']),
                         msg='We do not care for other errors in the command line if the --version option is present')

        self.assertEqual(0, self.call_with_args(['--solc', 'solc42', '--version']),
                         msg='We do not care for other errors in the command line if the --version option is present')

        self.assertNotEqual(0, self.call_with_args(['--solc', 'solc42', '--versions']),
                            msg='--versions is not --version')
        self.assertNotEqual(0, self.call_with_args(['--solc', 'solc42', '--ver']),
                            msg='--ver is not --version')
