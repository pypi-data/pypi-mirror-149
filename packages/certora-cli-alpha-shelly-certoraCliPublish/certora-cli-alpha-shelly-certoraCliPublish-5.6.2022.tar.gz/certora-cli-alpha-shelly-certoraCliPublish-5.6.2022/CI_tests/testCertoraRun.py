import unittest
import argparse
import os
from typing import List, Dict, Set, Any
import subprocess
import sys
from stat import S_IXUSR, S_IWUSR, S_IRUSR
import json
from pathlib import Path

scripts_dir_path = Path(__file__).parent.parent.resolve()  # one directory up
sys.path.insert(0, str(scripts_dir_path))
from Shared.certoraUtils import remove_file, is_ci_or_git_action
import certoraRun


class TestOptionTypes(unittest.TestCase):
    def test_type_jar(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_jar('blah')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_jar('')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_jar('blah.py')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_jar('blah.jar')
        with self.assertRaises(argparse.ArgumentTypeError, msg='path is a directory, not a file'):
            certoraRun.type_jar('..')

        with open('tmp.py', 'w') as f:
            f.write("print('hi')")
        with self.assertRaises(argparse.ArgumentTypeError, msg='file is not of type .jar'):
            certoraRun.type_jar('tmp.py')
        remove_file('tmp.py')

        with open('tmp.jar', 'w') as f:
            f.write("print('hi')")
        os.chmod('tmp.jar', S_IRUSR | S_IWUSR | S_IXUSR)
        self.assertEqual(certoraRun.type_jar('tmp.jar'), 'tmp.jar', msg='valid argument')
        remove_file('tmp.jar')

        with open('Alpha_Numeric_012-3.jar', 'w') as f:
            f.write("print('hi')")
        os.chmod('Alpha_Numeric_012-3.jar', S_IRUSR | S_IWUSR | S_IXUSR)
        self.assertEqual(certoraRun.type_jar('Alpha_Numeric_012-3.jar'), 'Alpha_Numeric_012-3.jar',
                         msg='valid argument')
        remove_file('Alpha_Numeric_012-3.jar')

        illegal_names = ['bad name', 'b@d_name']
        for illegal_name in illegal_names:
            filename = illegal_name + '.jar'
            with open(filename, 'w') as f:
                f.write("print('hi')")
            os.chmod(filename, S_IRUSR | S_IWUSR | S_IXUSR)
            with self.assertRaises(argparse.ArgumentTypeError, msg='file name contains illegal characters'):
                certoraRun.type_jar(filename)
            remove_file(filename)

    def test_type_a_file(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_readable_file('blah')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_readable_file('')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_readable_file('blah.py')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_readable_file('blah.jar')
        with self.assertRaises(argparse.ArgumentTypeError, msg='path is a directory, not a file'):
            certoraRun.type_readable_file('..')
        with self.assertRaises(argparse.ArgumentTypeError, msg='path is a directory, not a file'):
            certoraRun.type_readable_file('../..')

        with open('tmp.txt', 'w') as f:
            f.write("print('hi')")
        self.assertEqual(certoraRun.type_readable_file('tmp.txt'), 'tmp.txt', msg='valid argument')
        remove_file('tmp.txt')

    def test_type_dir(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_dir('blah')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_dir('')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_dir('blah.py')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_dir('blah.jar')

        with open('tmp.txt', 'w') as f:
            f.write("print('hi')")
        with self.assertRaises(argparse.ArgumentTypeError, msg='path is a file, not a directory'):
            certoraRun.type_dir('tmp.txt')
        remove_file('tmp.txt')

        self.assertEqual(certoraRun.type_dir('.'), Path('.').resolve().as_posix(), msg='valid argument')
        self.assertEqual(certoraRun.type_dir('..'), Path('..').resolve().as_posix(), msg='valid argument')

    def test_type_list(self) -> None:
        with self.assertRaises(ValueError, msg='not a list'):
            certoraRun.type_list('blah')
        with self.assertRaises(SyntaxError, msg='not a list'):
            certoraRun.type_list('')
        with self.assertRaises(SyntaxError, msg='not a list'):
            certoraRun.type_list('[[')
        with self.assertRaises(argparse.ArgumentTypeError, msg='not a list'):
            certoraRun.type_list('()')
        with self.assertRaises(SyntaxError, msg='not a list'):
            certoraRun.type_list('\\9')

        self.assertEqual([], certoraRun.type_list('[]'), msg='valid argument, empty list')
        self.assertEqual(['--verify', '--assert'], certoraRun.type_list("['--verify', '--assert']"),
                         msg='valid argument')

    def test_type_input_file(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_input_file('blah')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_input_file('')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_input_file('blah.py')
        with self.assertRaises(argparse.ArgumentTypeError, msg='file does not exist'):
            certoraRun.type_input_file('blah.jar')

        with open('tmp.sol', 'w') as f:
            f.write("print('hi')")
        self.assertEqual(certoraRun.type_input_file('tmp.sol'), 'tmp.sol', msg='valid argument Solidity file')
        self.assertEqual(certoraRun.type_input_file('tmp.sol:Monarch'), 'tmp.sol:Monarch', msg='valid argument')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_input_file('tmp.sol:El:Paso')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='contract names can contain only alphanumeric characters or underscores'):
            certoraRun.type_input_file('tmp.sol:El Paso')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='contract names can contain only alphanumeric characters or underscores'):
            certoraRun.type_input_file('tmp.sol:El-Paso')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='contract names can contain only alphanumeric characters or underscores'):
            certoraRun.type_input_file('tmp.sol:El.Paso')
        remove_file('tmp.sol')

        with open('pad thai.sol', 'w') as f:
            f.write("print('hi')")
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg="only alphanumeric characters and underscores are allowed in file names"):
            certoraRun.type_input_file('pad thai.sol')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg="only alphanumeric characters and underscores are allowed in file names"):
            certoraRun.type_input_file('pad thai.sol:Curry')
        remove_file('pad thai.sol')

        with open('tmp.conf', 'w') as f:
            f.write("print('hi')")
        self.assertEqual(certoraRun.type_input_file('tmp.conf'), 'tmp.conf', msg='valid argument .conf file')
        with self.assertRaises(argparse.ArgumentTypeError, msg='.conf files cannot contain contracts'):
            certoraRun.type_input_file('tmp.conf:Godzilla')
        remove_file('tmp.conf')

        with open('tmp.tac', 'w') as f:
            f.write("print('hi')")
        self.assertEqual(certoraRun.type_input_file('tmp.tac'), 'tmp.tac', msg='valid argument .tac file')
        with self.assertRaises(argparse.ArgumentTypeError, msg='.tac files cannot have contracts'):
            certoraRun.type_input_file('tmp.tac:Godzilla')
        remove_file('tmp.tac')

    def test_type_verify_arg(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('blah')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('blah.py')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('blah.jar')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('casino:royal')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('casino:royal.spec')

        with open('rangers.conf', 'w') as f:
            f.write("print('hi')")
        with self.assertRaises(argparse.ArgumentTypeError, msg='verify arg must get either a .spec or .cvl file'):
            certoraRun.type_verify_arg('power:rangers.conf')
        remove_file('rangers.conf')

        # Now let's create a valid spec file
        with open('dc.spec', 'w') as f:
            f.write("thunderstruck")

        # good usage
        self.assertEqual(certoraRun.type_verify_arg('ac:dc.spec'), 'ac:dc.spec', msg='valid argument .tac file')

        # bad usage
        with self.assertRaises(argparse.ArgumentTypeError, msg='invalid character dot in contract name'):
            certoraRun.type_verify_arg('ac.spec:dc.spec')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg(':dc.spec')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('a:c:dc.spec')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('a:dc.spec:c')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('dc.spec:a')
        with self.assertRaises(argparse.ArgumentTypeError, msg='wrong format'):
            certoraRun.type_verify_arg('dc.spec:a.spec')
        with self.assertRaises(argparse.ArgumentTypeError, msg='illegal character - in contract name'):
            certoraRun.type_verify_arg('New-York:dc.spec')
        with self.assertRaises(argparse.ArgumentTypeError, msg='illegal character space in contract name'):
            certoraRun.type_verify_arg('New York:dc.spec')
        with self.assertRaises(argparse.ArgumentTypeError, msg='illegal character / in contract name'):
            certoraRun.type_verify_arg('New/York:dc.spec')

        remove_file('dc.spec')

    def test_verify_files_input(self) -> None:
        # This function does NOT check if the files exist, or correct formatting. It checks file type consistency
        certoraRun.check_files_input(['blah.tac'])
        certoraRun.check_files_input(['blah.conf'])
        certoraRun.check_files_input(['blah.sol'])
        certoraRun.check_files_input(['blah.sol', 'blah.sol'])
        certoraRun.check_files_input(['blah.sol', '.sol'])
        certoraRun.check_files_input(['blah.sol:blah', '.sol'])

        with self.assertRaises(argparse.ArgumentTypeError, msg='cannot get both .tac and Solidity files'):
            certoraRun.check_files_input(['blah.sol', 'blah.tac'])
        with self.assertRaises(argparse.ArgumentTypeError, msg='cannot get both .conf and Solidity files'):
            certoraRun.check_files_input(['blah.sol', 'blah.conf'])
        with self.assertRaises(argparse.ArgumentTypeError, msg='cannot get both .tac and .conf files'):
            certoraRun.check_files_input(['blah.tac', 'blah.conf'])
        with self.assertRaises(argparse.ArgumentTypeError, msg='cannot get both .tac and .conf files'):
            certoraRun.check_files_input(['blah.conf', 'blah.tac'])

        with self.assertRaises(argparse.ArgumentTypeError, msg='cannot get both .tac and Solidity files'):
            certoraRun.check_files_input(['a.conf', 'b.sol', 'c.sol', 'd.tac', 'e.sol:f'])
        with self.assertRaises(argparse.ArgumentTypeError, msg='cannot get both .tac and Solidity files'):
            certoraRun.check_files_input(['a.conf', 'b.sol', 'c.sol', 'd.sol', 'e.sol:f', 'g.tac'])

    def test_type_link_arg(self) -> None:
        self.assertEqual('A:b=C', certoraRun.type_link_arg('A:b=C'), msg='valid argument')
        self.assertEqual('A:b=A', certoraRun.type_link_arg('A:b=A'), msg='valid argument')
        self.assertEqual('A:b=b', certoraRun.type_link_arg('A:b=b'), msg='valid argument')
        self.assertEqual('A:A=b', certoraRun.type_link_arg('A:A=b'), msg='valid argument')
        self.assertEqual('A:A=A', certoraRun.type_link_arg('A:A=A'), msg='valid argument')
        self.assertEqual('A:b=15', certoraRun.type_link_arg('A:b=15'), msg='valid argument')
        self.assertEqual('A:b=0x1', certoraRun.type_link_arg('A:b=0x1'), msg='valid argument')
        self.assertEqual('A:b=0xc', certoraRun.type_link_arg('A:b=0xc'), msg='valid argument')
        self.assertEqual('A:b=0Xc', certoraRun.type_link_arg('A:b=0Xc'), msg='valid argument')
        self.assertEqual('A:b=0XC', certoraRun.type_link_arg('A:b=0XC'), msg='valid argument')
        self.assertEqual('A:b=0xC', certoraRun.type_link_arg('A:b=0xC'), msg='valid argument')
        self.assertEqual('A:b=0X1', certoraRun.type_link_arg('A:b=0X1'), msg='valid argument')

        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_link_arg('A:=B')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A=B'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A:B'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A:B:C=D'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A:B=C=D'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A:B<D'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A.b=C'))

        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A:b=C++'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A:b==C'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A:b=AC/DC'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A:b=new-york'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('A:queen-size=J'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_link_arg('Ca$h:queen=J'))

    def test_type_struct_link(self) -> None:
        self.assertEqual('A:1=C', certoraRun.type_struct_link('A:1=C'), msg='valid argument')
        self.assertEqual('A:0=C', certoraRun.type_struct_link('A:0=C'), msg='valid argument')
        self.assertEqual('A:1529876=C', certoraRun.type_struct_link('A:1529876=C'), msg='valid argument')
        self.assertEqual('Joseph:1529876=Smith', certoraRun.type_struct_link('Joseph:1529876=Smith'),
                         msg='valid argument')

        with self.assertRaises(argparse.ArgumentTypeError, msg='negative number is illegal'):
            self.assertEqual(None, certoraRun.type_struct_link('A:-1=C'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='only integers allowed'):
            self.assertEqual(None, certoraRun.type_struct_link('A:0.1=C'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='missing number'):
            self.assertEqual(None, certoraRun.type_struct_link('A=C'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='missing number'):
            self.assertEqual(None, certoraRun.type_struct_link('A1=C'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link('C=A:1'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link('1:A.f=C'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link('A:3'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link('A=3'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link('A:=3'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link('A:=C'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link(':3=C'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link(':=C'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link(':='))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link(':'))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link('='))
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            self.assertEqual(None, certoraRun.type_struct_link(''))

    def test_type_contract_name(self) -> None:
        self.assertEqual('A', certoraRun.type_contract('A'), msg='valid argument')
        self.assertEqual('contract', certoraRun.type_contract('contract'), msg='valid argument')

        with self.assertRaises(argparse.ArgumentTypeError, msg='A contract name cannot have a .jar suffix'):
            self.assertEqual(None, certoraRun.type_contract('a.jar'))

        with self.assertRaises(argparse.ArgumentTypeError, msg='A contract name cannot have a .py suffix'):
            self.assertEqual(None, certoraRun.type_contract('b.py'))

        with self.assertRaises(argparse.ArgumentTypeError, msg='A contract name cannot have a .sol suffix'):
            self.assertEqual(None, certoraRun.type_contract('.sol'))

        with self.assertRaises(argparse.ArgumentTypeError, msg='A contract name cannot have a .sol suffix'):
            self.assertEqual(None, certoraRun.type_contract('contract.sol'))

        with self.assertRaises(argparse.ArgumentTypeError, msg='A contract name cannot have a .sol suffix'):
            self.assertEqual(None, certoraRun.type_contract('a.sol.sol'))

    def test_type_package(self) -> None:
        self.assertEqual('a=.', certoraRun.type_package('a=.'), msg='valid argument')
        self.assertEqual('a.sol=..', certoraRun.type_package('a.sol=..'), msg='valid argument')

        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_package('a')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_package('a.sol')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_package('a=')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_package('a=bb')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_package('=.')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_package('=')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_package('a=b=c')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_package('a==b')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_package('a:b')

    def test_get_trivial_contract_name(self) -> None:
        self.assertEqual('a', certoraRun._get_trivial_contract_name('a.sol'))
        self.assertEqual('blipblop', certoraRun._get_trivial_contract_name('blipblop.sol'))
        self.assertEqual('b', certoraRun._get_trivial_contract_name('a/b.sol'))
        self.assertEqual('b', certoraRun._get_trivial_contract_name('../abiglib/./b.sol'))
        self.assertEqual('b', certoraRun._get_trivial_contract_name('~/b.sol'))
        self.assertEqual('b', certoraRun._get_trivial_contract_name('a\\b.sol'))
        self.assertEqual('b', certoraRun._get_trivial_contract_name('C:\\b.sol'))
        self.assertEqual('b', certoraRun._get_trivial_contract_name('D:\\a\\b.sol'))

    def test_warn_verify_file_args(self) -> None:
        def __test_equality(args: List[str], contracts: Set[str], files: Set[str],
                            contract_to_file: Dict[str, str], file_to_contract: Dict[str, str]) -> None:
            _contracts, _files, _contract_to_file, _file_to_contract = certoraRun.warn_verify_file_args(args)
            self.assertSetEqual(contracts, _contracts, msg="contract name set should be equal")
            self.assertSetEqual(files, _files, msg="file path set should be equal")
            self.assertDictEqual(contract_to_file, contract_to_file, msg="contract to file map should be equal")
            self.assertDictEqual(file_to_contract, _file_to_contract, msg="file to contract map should be equal")

        __test_equality(['A.sol'], {'A'}, {'A.sol'}, {'A': 'A.sol'}, {'A.sol': 'A'})
        __test_equality(['A.sol:a'], {'a'}, {'A.sol'}, {'a': 'A.sol'}, {'A.sol': 'a'})
        __test_equality(['A.sol:a', 'B.sol'], {'a', 'B'}, {'A.sol', 'B.sol'}, {'a': 'A.sol', 'B': 'B.sol'},
                        {'A.sol': 'a', 'B.sol': 'B'})
        __test_equality(['A.sol:a', 'B.sol:b'], {'a', 'b'}, {'A.sol', 'B.sol'}, {'a': 'A.sol', 'b': 'B.sol'},
                        {'A.sol': 'a', 'B.sol': 'b'})
        __test_equality(['A.sol:a', 'B.sol:b', 'c.sol'], {'a', 'b', 'c'}, {'A.sol', 'B.sol', 'c.sol'},
                        {'a': 'A.sol', 'b': 'B.sol', 'c': 'c.sol'},
                        {'A.sol': 'a', 'B.sol': 'b', 'c.sol': 'c'})

        __test_equality(['A.sol', 'A.sol'], {'A'}, {'A.sol'}, {'A': 'A.sol'}, {'A.sol': 'A'})
        __test_equality(
            ['folder/A.sol', 'folder/A.sol'], {'A'}, {'folder/A.sol'}, {'A': 'folder/A.sol'}, {'folder/A.sol': 'A'})
        __test_equality(['A.sol:a', 'A.sol:a'], {'a'}, {'A.sol'}, {'a': 'A.sol'}, {'A.sol': 'a'})
        __test_equality(['folder/A.sol:a', 'folder\\A.sol:a'], {'a'}, {'folder/A.sol'}, {'a': 'folder/A.sol'},
                        {'folder/A.sol': 'a'})

        __test_equality(['folder/A.sol', 'folder/../folder/A.sol'], {'A'}, {'folder/A.sol'}, {'A': 'folder/A.sol'},
                        {'folder/A.sol': 'A'})
        __test_equality(['A.sol', './A.sol'], {'A'}, {'A.sol'}, {'A': 'A.sol'}, {'A.sol': 'A'})

        __test_equality(['A.sol:A'], {'A'}, {'A.sol'}, {'A': 'A.sol'}, {'A.sol': 'A'})
        __test_equality(['A.sol:A', 'A.sol'], {'A'}, {'A.sol'}, {'A': 'A.sol'}, {'A.sol': 'A'})
        __test_equality(['A.sol:A', 'A.sol:A', 'A.sol'], {'A'}, {'A.sol'}, {'A': 'A.sol'}, {'A.sol': 'A'})
        __test_equality(['A.sol:B', 'B.sol:c'], {'B', 'c'}, {'A.sol', 'B.sol'}, {'B': 'A.sol', 'c': 'B.sol'},
                        {'A.sol': 'B', 'B.sol': 'c'})

        # Case sensitivity test
        __test_equality(['car.sol', 'Car.sol', 'CAR.sol'], {'car', 'CAR', 'Car'}, {'car.sol', 'Car.sol', 'CAR.sol'},
                        {'car': 'car.sol', 'Car': 'Car.sol', 'CAR': 'CAR.sol'},
                        {'car.sol': 'car', 'Car.sol': 'Car', 'CAR.sol': 'CAR'})

        with self.assertRaises(argparse.ArgumentTypeError, msg='A file cannot have two different names'):
            certoraRun.warn_verify_file_args(['A.sol', 'A.sol:a'])
        with self.assertRaises(argparse.ArgumentTypeError, msg='A file cannot have two different names'):
            certoraRun.warn_verify_file_args(['A.sol:a', 'A.sol'])
        with self.assertRaises(argparse.ArgumentTypeError, msg='A file cannot have two different names'):
            certoraRun.warn_verify_file_args(['A.sol:a', 'A.sol:b'])

        with self.assertRaises(argparse.ArgumentTypeError, msg='Two files cannot have the same name'):
            certoraRun.warn_verify_file_args(['A.sol:a', 'B.sol:a'])

        with self.assertRaises(argparse.ArgumentTypeError, msg='Two files cannot have the same name'):
            certoraRun.warn_verify_file_args(['./A.sol', '../some/dir/A.sol'])

        # warnings + errors should be errors
        with self.assertRaises(argparse.ArgumentTypeError, msg='Two files cannot have the same name'):
            certoraRun.warn_verify_file_args(['A.sol:A', './A.sol', '../some/dir/A.sol'])

    def test_type_non_negative_int(self) -> None:
        self.assertEqual('0', certoraRun.type_non_negative_integer('0'), msg='valid argument')
        self.assertEqual('1', certoraRun.type_non_negative_integer('1'), msg='valid argument')
        self.assertEqual('345', certoraRun.type_non_negative_integer('345'), msg='valid argument')

        with self.assertRaises(argparse.ArgumentTypeError, msg='negative int'):
            certoraRun.type_non_negative_integer('-1')
        with self.assertRaises(argparse.ArgumentTypeError, msg='negative int'):
            certoraRun.type_non_negative_integer('-1890')
        with self.assertRaises(argparse.ArgumentTypeError, msg='not an integer'):
            certoraRun.type_non_negative_integer('0.01')
        with self.assertRaises(argparse.ArgumentTypeError, msg='not an integer'):
            certoraRun.type_non_negative_integer('2.0000')
        with self.assertRaises(argparse.ArgumentTypeError, msg='not an integer'):
            certoraRun.type_non_negative_integer('3e-9')
        with self.assertRaises(argparse.ArgumentTypeError, msg='not a decimal integer'):
            certoraRun.type_non_negative_integer('0x12d')
        with self.assertRaises(argparse.ArgumentTypeError, msg='not a decimal integer'):
            certoraRun.type_non_negative_integer('0X12d')
        with self.assertRaises(argparse.ArgumentTypeError, msg='not a decimal integer'):
            certoraRun.type_non_negative_integer('0XFF')

    def test_type_solc_map(self) -> None:
        self.assertDictEqual({'a': 'solc6.10'}, certoraRun.type_solc_map('a=solc6.10'), msg='valid argument')
        self.assertDictEqual({'a': 'solc6.10', 'b': 'solc4.25'}, certoraRun.type_solc_map('a=solc6.10,b=solc4.25'),
                             msg='valid argument')
        self.assertDictEqual({'a': 'solc6.10'}, certoraRun.type_solc_map('a=solc6.10,a=solc6.10'),
                             msg='providing the same mapping multiple times is redundant but legal')

        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_solc_map('whataburger')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_solc_map('1.5')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_solc_map('solc4.25')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_solc_map('=solc4.25')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_solc_map('a=')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_solc_map('=')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad format'):
            certoraRun.type_solc_map(',')
        with self.assertRaises(argparse.ArgumentTypeError, msg='comma at the end'):
            certoraRun.type_solc_map('a=solc4.25,')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad delimiter'):
            certoraRun.type_solc_map('a:solc4.25')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad delimiter'):
            certoraRun.type_solc_map('a==solc4.25')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad delimiter'):
            certoraRun.type_solc_map('a=,b=solc4.25')
        with self.assertRaises(argparse.ArgumentTypeError, msg='bad delimiter'):
            certoraRun.type_solc_map('a,=solc4.25')
        with self.assertRaises(argparse.ArgumentTypeError, msg='comma at the beginning'):
            certoraRun.type_solc_map(',a=solc4.25')

        with self.assertRaises(argparse.ArgumentTypeError, msg='comma at the beginning'):
            certoraRun.type_solc_map('a=solc4.25,a=solc6.10')

        # Using --solc and --solc_map together is an error
        # maybe solc_map can output a map!

    def test_type_method(self) -> None:
        self.assertEqual('foo()', certoraRun.type_method('foo()'), msg='method without arguments')
        self.assertEqual('foo(uint256)', certoraRun.type_method('foo(uint256)'), msg='method with arguments')
        self.assertEqual('foo(bool)', certoraRun.type_method('foo(bool)'), msg='method with arguments')
        self.assertEqual('foo(bool,bool)', certoraRun.type_method('foo(bool,bool)'), msg='method with two arguments')
        self.assertEqual('foo_bar(bool)', certoraRun.type_method('foo_bar(bool)'), msg='method name with underscore')
        self.assertEqual('foo_bar(address payable)', certoraRun.type_method('foo_bar(address payable)'),
                         msg='method with address payable parameter')
        self.assertEqual('foo_bar(uint[], address payable[])',
                         certoraRun.type_method('foo_bar(uint[], address payable[])'),
                         msg='method with square brackets')
        self.assertEqual('foo((bool, bool))',
                         certoraRun.type_method('foo((bool, bool))'),
                         msg='method with a simple struct')
        self.assertEqual('foo((bool, bool), address, (uint258))',
                         certoraRun.type_method('foo((bool, bool), address, (uint258))'),
                         msg='method with two structs')
        self.assertEqual('foo((bool, bool, (bool, bool)))',
                         certoraRun.type_method('foo((bool, bool, (bool, bool)))'),
                         msg='method with a nested struct')

        with self.assertRaises(argparse.ArgumentTypeError, msg='malformed --method argument - no parenthesis'):
            certoraRun.type_method('foo')
        with self.assertRaises(argparse.ArgumentTypeError, msg='malformed --method argument - no closing parenthesis'):
            certoraRun.type_method('foo(')
        with self.assertRaises(argparse.ArgumentTypeError, msg='malformed --method argument - no opening parenthesis'):
            certoraRun.type_method('foo)')
        with self.assertRaises(argparse.ArgumentTypeError, msg='malformed --method argument - unordered parenthesis'):
            certoraRun.type_method('foo)(')
        with self.assertRaises(argparse.ArgumentTypeError, msg='malformed --method argument - an empty struct'):
            certoraRun.type_method('foo(())')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - too many opening parenthesis'):
            certoraRun.type_method('foo()()')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - no method name'):
            certoraRun.type_method('()')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - no method name'):
            certoraRun.type_method('(bool)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - no method name'):
            certoraRun.type_method('(bool, uint)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - no parameter type'):
            certoraRun.type_method('bar(bool,)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - no parameter type'):
            certoraRun.type_method('bar(,bool)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - no parameter type'):
            certoraRun.type_method('bar(,)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - has whitespace'):
            certoraRun.type_method('bar(, )')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - has unsupported character'):
            certoraRun.type_method('bar(bool#)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - has unsupported character'):
            certoraRun.type_method('bar($)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - function name cannot contain a comma'):
            certoraRun.type_method('foo,()')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - missing closing bracket'):
            certoraRun.type_method('foo,(bool[)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - missing closing bracket'):
            certoraRun.type_method('foo,(bool[, bool)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - missing opening bracket'):
            certoraRun.type_method('foo,(bool])')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - missing opening bracket'):
            certoraRun.type_method('foo,(bool], bool)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - missing primitive type for brackets'):
            certoraRun.type_method('foo,([], bool)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - missing primitive type for brackets'):
            certoraRun.type_method('foo,(], bool)')
        with self.assertRaises(argparse.ArgumentTypeError,
                               msg='malformed --method argument - arg inside brackets'):
            certoraRun.type_method('foo,(bool[bool])')


class TestCLIArgs(unittest.TestCase):
    certora_run_path = str(Path(__file__).parent.parent / 'certoraRun.py')
    default_path = Path.cwd() / 'contracts'

    @staticmethod
    def call_with_args(cli_args: List[str], add_solc: bool = True) -> int:
        argv = [sys.executable, TestCLIArgs.certora_run_path] + cli_args + ['--check_args']

        if add_solc and '--solc' not in argv:
            argv += ['--solc', 'solc6.10']
        print(f"Running with: {argv}")
        # res = subprocess.call(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        res = subprocess.call(argv)  # use this line for debugging, the line above suppresses output
        return res  # 0 is success

    @staticmethod
    def call_and_run_with_args(cli_args: List[str], add_solc: bool = True, solc_ver: str = 'solc6.10') -> int:
        argv = [sys.executable, TestCLIArgs.certora_run_path] + cli_args

        if add_solc and '--solc' not in argv:
            argv += ['--solc', solc_ver]
        # res = subprocess.call(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        res = subprocess.call(argv)  # use this line for debugging, the line above suppresses output
        return res  # 0 is success

    def setUp(self) -> None:
        sol_files = ['paris', 'rome', 'madrid', 'london']

        for sol_f in sol_files:
            with open(sol_f + '.sol', 'w') as f:
                f.write("Europe")

        with open('solc', 'w') as f:
            f.write('this compiles Solidity')

        if not TestCLIArgs.default_path.exists():
            TestCLIArgs.default_path.mkdir()

        with open('spec.spec', 'w') as f:
            f.write('A -> B')

    def tearDown(self) -> None:
        sol_files = ['paris', 'rome', 'madrid', 'london']
        for solf in sol_files:
            remove_file(solf + '.sol')

        remove_file('solc')
        remove_file('spec.spec')
        TestCLIArgs.default_path.rmdir()

    def test_help(self) -> None:
        self.assertEqual(0, self.call_with_args(['--help']), msg='typical use case')
        self.assertEqual(0, self.call_with_args(['--help', 'Akroma']),
                         msg='We do not care for other errors in the command line if the --help option is present')
        self.assertEqual(0, self.call_with_args(['Akroma', '--help']),
                         msg='We do not care for other errors in the command line if the --help option is present')
        self.assertEqual(0, self.call_with_args(['--solc', 'solc42', '--help']),
                         msg='We do not care for other errors in the command line if the --help option is present')

        self.assertNotEqual(0, self.call_with_args(['--solc', 'solc42', '--helps']),
                            msg='--helps is not --help')
        self.assertNotEqual(0, self.call_with_args(['--solc', 'solc42', '--hel']),
                            msg='--hel is not --help')

    def test_basic(self) -> None:
        self.assertNotEqual(0, self.call_with_args([]), msg='prover must get arguments')
        self.assertNotEqual(0, self.call_with_args(['fake_file']), msg='fake_file does not exist')
        self.assertNotEqual(0, self.call_with_args(['rome.sol']), msg='either --assert or --verify must be used')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert']), msg='--assert must be given a contract')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome']),
                         msg='minimal run of the Certora prover')

    def test_file_arguments(self) -> None:

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome']),
                         msg='minimal run of the Certora prover')
        self.assertEqual(0, self.call_with_args(['rome.sol:B', '--assert', 'B']),
                         msg='minimal run of the Certora prover with a contract name')

        self.assertEqual(0, self.call_with_args(['rome.sol', 'london.sol', '--assert', 'rome']),
                         msg='running the prover with multiple input files')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'london.sol', '--assert', 'london', 'rome']),
                         msg='running the prover with multiple input files')

        self.assertNotEqual(0, self.call_with_args(['rome.sol:B:C', '--assert', 'B']),
                            msg='Too many : signs')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:El-Paso', '--assert', 'B']),
                            msg='Contract name contained illegal character -')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:El Paso', '--assert', 'B']),
                            msg='Contract name contained illegal character space')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:El.Paso', '--assert', 'B']),
                            msg='Contract name contained illegal character .')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:El/Paso', '--assert', 'B']),
                            msg='Contract name contained illegal character /')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:B', '--assert', 'rome']),
                            msg='no file named rome (it is named B)')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:A', 'rome.sol:B', '--assert', 'A']),
                            msg='A file might only include one contract name currently')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:tmp.sol', '--assert', 'rome']),
                            msg='The file is named tmp, not rome')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:tmp.tac', '--assert', 'tmp']),
                            msg='The file is named tmp.tac, not tmp')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:tmp.conf', '--assert', 'tmp']),
                            msg='The file is named tmp.conf, not tmp')

        self.assertEqual(0, self.call_with_args(['rome.sol:a', 'madrid.sol:b', '--assert', 'a']),
                         msg='multiple inputs files and multiples contract names, all legal')
        self.assertEqual(0, self.call_with_args(['rome.sol:tmp', 'london.sol:temp', '--assert', 'temp']),
                         msg='multiple inputs files and multiples contract names, all legal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:tmp', 'madrid.sol:tmp', '--assert', 'tmp']),
                            msg='Two different files were given the same name')

        self.assertEqual(0, self.call_with_args(['rome.sol:a', 'rome.sol:a', '--assert', 'a']),
                         msg='Giving the same input file and name twice is redundant, but not an error')
        self.assertEqual(0, self.call_with_args(['rome.sol:a', './rome.sol:a', '--assert', 'a']),
                         msg='Giving the same input file and name twice is redundant, but not an error')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:a', 'rome.sol', '--assert', 'rome']),
                            msg='File rome.sol must have a single name, here it will get two: rome and a')
        self.assertEqual(0, self.call_with_args(['rome.sol:rome', '--assert', 'rome']),
                         msg='Giving a file a name that is also his natural name is redundant, but legal')

        with open('tmp.tac', 'w') as f:
            f.write("keep Austin weird")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', 'tmp.tac', '--assert', 'rome']),
                            msg='A user cannot give both a Solidity and a .tac file')
        self.assertNotEqual(0, self.call_with_args(['tmp.tac:fort_worth', '--assert', 'rome']),
                            msg='A .tac file cannot contain a contract')

        with open('tmp.conf', 'w') as f:
            f.write("don't mess with Texas")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', 'tmp.conf', '--assert', 'rome']),
                            msg='A user cannot give both a Solidity and a .conf file')
        self.assertNotEqual(0, self.call_with_args(['tmp.conf:dallas', '--assert', 'rome']),
                            msg='A .conf file cannot contain a contract')
        self.assertNotEqual(0, self.call_with_args(['rome.tac', 'tmp.conf', '--assert', 'rome']),
                            msg='A user cannot give both a .tac and a .conf file')

        remove_file('tmp.tac')
        remove_file('tmp.conf')

    def test_assert_arguments(self) -> None:

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome']),
                         msg='typical use of --assert')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol', '--assert', 'rome', 'madrid']),
                         msg='typical use of --assert with multiples arguments')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', 'rome']),
                         msg='giving the same --assert argument twice is redundant, but not an error')

        self.assertNotEqual(0, self.call_with_args([]), msg='must provide files')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:A', '--assert', 'rome.sol']),
                            msg='contract name is rome not rome.sol')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:A', '--assert', 'rome']),
                            msg='contract name is A, not rome')
        self.assertEqual(0, self.call_with_args(['rome.sol:A', '--assert', 'A']),
                         msg='typical use of --assert with a contract name')
        self.assertNotEqual(0, self.call_with_args(['rome.sol:A', '--assert', 'A.sol']),
                            msg='contract name is A not A.sol')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert']), msg='--assert must be given an argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'qwwww']),
                            msg='qwwww is not a contract name')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome.tac']),
                            msg='rome.tac is not a contract name')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'sudden.sol']),
                            msg='sudden.sol is not a contract name')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', './rome.sol']),
                            msg='./rome.sol is not a contract name')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', '../a/path/rome.sol']),
                            msg='../a/path/rome.sol is not a contract name')

        # assert can be given multiple times
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol', '--assert', 'rome', '--assert', 'madrid']),
                         msg='using --assert multiple times is allowed')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol', '--assert', 'rome', '--cache', 'bash',
                                                 '--assert', 'madrid']),
                         msg='using --assert multiple times is allowed')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--assert', 'rome']),
                         msg='using --assert multiple times is allowed, giving the same argument twice is redundant but'
                             ' not an error')

    def test_verify_arguments(self) -> None:
        spec_files = ['sonora', 'chihuahua']

        for specification in spec_files:
            with open(specification + '.spec', 'w') as f:
                f.write("viva la revolution")

        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:sonora.spec']),
                         msg='typical use of --verify')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:sonora.spec',
                                                 'rome:sonora.spec']),
                         msg='--verify was given the same argument twice, redundant but not an error')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:sonora.spec',
                                                 'rome:chihuahua.spec']),
                         msg='typical use of --verify, a contract can be verified by several different specs')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol:gd', '--verify', 'rome:sonora.spec',
                                                 'rome:chihuahua.spec', 'gd:sonora.spec', 'gd:chihuahua.spec']),
                         msg='typical use of --verify, giving multiple contracts and specs')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome.sol:sonora.spec']),
                            msg="a contract's name cannot contain non-alphanumeric characters like a dot")
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify']),
                            msg='--verify must be given an argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', 'london.sol:sonora.spec']),
                            msg='--verify was given an undefined contract london.sol')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:sonora']),
                            msg='sonora is not an existing file (sonora.spec is)')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:quintana.spec']),
                            msg='file quintana.spec does not exist')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:rome']),
                            msg='rome is a Solidity file, not a .spec file')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:rome.sol']),
                            msg='rome.sol is a Solidity file, not a .spec file')

        # multiple --verify usages are allowed:
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol:gd', '--verify', 'rome:sonora.spec',
                                                 'rome:chihuahua.spec', '--cache', 'IBM', '--verify', 'gd:sonora.spec',
                                                 'gd:chihuahua.spec']),
                         msg='using --verify multiple times is allowed')

        # Checking .cvl files too

        with open('berlin.cvl', 'w') as f:
            f.write('Unter den Linden')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:berlin.cvl']),
                         msg='--verify accepts .cvl files')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:berlin.cvl',
                                                 'rome:berlin.cvl']),
                         msg='--verify was given the same argument twice, redundant but not an error')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:sonora.spec',
                                                 'rome:berlin.cvl']),
                         msg='--verify accepts either .spec or .cvl files interchangeably')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol:gd', '--verify', 'rome:sonora.spec',
                                                 'rome:chihuahua.spec', 'gd:sonora.spec', 'gd:berlin.cvl']),
                         msg='--verify accepts either .spec or .cvl files interchangeably')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', 'london.sol:berlin.cvl']),
                            msg='--verify was given an undefined contract london.sol')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:berlin']),
                            msg='file berlin does not exist')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:guanajuato.cvl']),
                            msg='file guanajuato.cvl does not exist')

        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol:gd', '--verify', 'rome:sonora.spec',
                                                 'rome:chihuahua.spec', '--cache', 'IBM', '--verify', 'gd:sonora.spec',
                                                 'gd:chihuahua.spec', 'gd:berlin.cvl']),
                         msg='using --verify multiple times is allowed')

        with open('community.tac', 'w') as f:
            f.write('Abed Nadir')

        self.assertNotEqual(0, self.call_with_args(['community.tac', '--verify', 'community:sonora.spec']),
                            msg='.tac files cannot be verified')

        remove_file('community.tac')

        with open('jeff.conf', 'w') as f:
            f.write('Walker')

        self.assertNotEqual(0, self.call_with_args(['jeff.conf', '--verify', 'jeff:sonora.spec']),
                            msg='.tac files cannot be verified')

        remove_file('jeff.conf')

        # Tear down
        for specification in spec_files:
            remove_file(specification + '.spec')
        remove_file('berlin.cvl')

    def test_link(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', 'paris.sol', '--assert', 'rome', '--link',
                                                 'rome:a=paris']),
                         msg='typical use of --link')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'paris.sol', '--assert', 'rome', '--link',
                                                 'rome:New_York_2=paris']),
                         msg='slot names can have alphanumeric characters and underscores')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=rome']),
                         msg='self linking is allowed')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'paris.sol', '--assert', 'rome', '--link',
                                                 'rome:a=paris', 'rome:a=paris']),
                         msg='defining the same link twice is redundant, but not an error')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'paris.sol', '--assert', 'rome', '--link',
                                                 'rome:a=paris', 'paris:b=rome']),
                         msg='two-way linking is allowed')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=12']),
                         msg='a link can accept a number')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=12',
                                                 'rome:rome=999']),
                         msg='a link can accept a number')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=0']),
                         msg='a link can accept the number zero')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=0xd3c']),
                         msg='a link can accept a hexadecimal number')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=0XD3C']),
                         msg='a link can accept a hexadecimal number')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=0Xd3c']),
                         msg='a link can accept a hexadecimal number')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link']),
                            msg='--link must be given an argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=0xx23']),
                            msg='--link was given a number in wrong format')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:c-type=0x23']),
                            msg='illegal character dash in slot name')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:new york=0x23']),
                            msg='illegal space in slot name')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:fuzzy= feeling']),
                            msg='illegal space')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:fuzzy= feeling']),
                            msg='illegal space')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome :fuzzy=feeling']),
                            msg='illegal space')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome: fuzzy=feeling']),
                            msg='illegal space')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:fuzzy =feeling']),
                            msg='illegal space')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:fuzzy=feel.ing']),
                            msg='illegal character .')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=-1']),
                            msg='--link cannot be given a negative number')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=1.65']),
                            msg='--link cannot be given a non-integer number')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=2e-3']),
                            msg='--link cannot be given a non-integer number')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=d']),
                            msg='--link must be given either a contract or a non-negative integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:paris']),
                            msg='--link must be given either a contract or a non-negative integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:bronze']),
                            msg='--link must be given either a contract or a non-negative integer')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--link', 'rome:a=0',
                                                    'rome:a=1']),
                            msg='the link rome:a was given two contradicting definitions')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', 'paris.sol', '--assert', 'rome', '--link',
                                                    'rome:a=0', 'rome:a=paris']),
                            msg='the link rome:a was given two contradicting definitions')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', 'paris.sol', '--assert', 'rome', '--link',
                                                    'rome:a=rome', 'rome:a=paris']),
                            msg='the link rome:a was given two contradicting definitions')

        # multiple invocations of the --link option are legal
        self.assertNotEqual(0, self.call_with_args(['rome.sol', 'paris.sol', '--assert', 'rome', '--link',
                                                    'rome:a=0', '--cache', 'bitcoin', '--link', 'rome:a=paris']),
                            msg='using --link multiple times is allowed')

        # tac and conf files cannot be linked

        with open('Charlie.tac', 'w') as f:
            f.write('Brown')

        self.assertNotEqual(0, self.call_with_args(['Charlie.tac', '--link', 'Charlie:a=Charlie']),
                            msg='cannot use --link with .tac file')
        remove_file('Charlie.tac')

        with open('Blue.conf', 'w') as f:
            f.write('Man Group')

        self.assertNotEqual(0, self.call_with_args(['Blue.conf', '--link', 'Blue:a=Blue']),
                            msg='cannot use --link with .conf file')
        remove_file('Blue.conf')

    def test_solc(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc', 'solc6.10']),
                         msg='typical use of --solc')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc']),
                            msg='--solc argument is a non-existent file')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc', 'solc1234']),
                            msg='--solc argument is a non-existent file')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc', '.']),
                            msg='--solc argument is a directory, not a file')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc', '"--optimize"']),
                            msg='--solc argument is a non-existent file (--solc_args argument was given instead)')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc',
                                                    '["--optimize", "--optimize-runs", "200"]']),
                            msg='--solc argument is a non-existent file (--solc_args argument was given instead)')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc',
                                                    '["--optimize", "--optimize-runs", 200"]']),
                            msg='--solc argument is a non-existent file (--solc_args argument was given instead)')

        # Avoid common mistakes
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc', 'rome.sol']),
                            msg='--solc argument was given a Solidity file')
        non_executable_files = ['henry.spec', 'george.tac', 'william.conf', 'harry.cvl']
        for non_ex in non_executable_files:
            with open(non_ex, 'w') as f:
                f.write('king')
            os.chmod(non_ex, S_IRUSR | S_IWUSR | S_IXUSR)
            self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc', non_ex]),
                                msg='--solc argument was given a non-executable file')
            remove_file(non_ex)

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc', 'solc6.10',
                                                    '--solc', 'solc6.10']),
                            msg='using --solc more than once is illegal')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc', 'solc6.10',
                                                    'solc6.10']),
                            msg='--solc must be given a single argument')

    def test_solc_args(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_args',
                                                 "['--optimize', '--optimize-runs', '200']"]),
                         msg='typical use case of --solc_args')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_args', "['--optimize']"]),
                         msg='typical use case of --solc_args')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_args', "[]"]),
                         msg='--solc_args can be given an empty list currently')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_args', "['']"]),
                         msg='--solc_args can be given empty list elements currently')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_args', "['', '', '']"]),
                         msg='--solc_args can be given empty list elements currently')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_args',
                                                 "['--optimize', '--optimize']"]),
                         msg='--solc_args can have redundant flags')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_args']),
                            msg='--solc_args must be given an argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_args', "['--optimize']",
                                                    '--solc_args', "['--optimize-runs']"]),
                            msg='using --solc_args more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_args', "['--optimize']",
                                                    '--solc_args', "['--optimize']"]),
                            msg='using --solc_args more than once is illegal')

    def test_solc_map(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_map', 'rome=solc6.10'],
                                                add_solc=False), msg='typical use of --solc_map')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol', '--assert', 'rome', 'madrid', '--solc_map',
                                                 'rome=solc6.10, madrid=solc4.25'], add_solc=False),
                         msg='typical use of --solc_map')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol', '--assert', 'rome', 'madrid', '--solc_map',
                                                 'rome=solc6.10,madrid=solc6.10'], add_solc=False),
                         msg='all arguments of --solc_map MAY have the same solidity version, it is just redundant')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_map',
                                                 'rome=solc6.10,rome=solc6.10'], add_solc=False),
                         msg='redundant argument in --solc_map is legal but discouraged by Uri')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_map', 'rome=solc6.10'],
                                                   add_solc=True), msg='cannot use --solc_args and --solc together')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--solc_map',
                                                    'rome=solc6.10,rome=solc4.25'], add_solc=False),
                            msg='contradicting definition in map')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', 'madrid.sol', '--assert', 'rome', 'madrid',
                                                    '--solc_map', 'rome=solc6.10'], add_solc=False),
                            msg='all contracts must appear in --solc_map, here madrid does not')

    def test_jar(self) -> None:
        with open('fake.jar', 'w') as f:
            f.write('this is a jar')
        os.chmod('fake.jar', S_IRUSR | S_IWUSR | S_IXUSR)

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar', 'fake.jar']),
                         msg='typical use of --jar')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar']),
                            msg='--jar must be given an argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar', 'cake']),
                            msg='--jar must be given an existing file path')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar', 'rome.sol']),
                            msg='--jar must be given a file path with executable permissions')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar', 'fake.jar',
                                                    '--jar', 'fake.jar']),
                            msg='using --jar more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar', 'fake.jar',
                                                    'fake.jar']),
                            msg='--jar must be given a single argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar', 'fake.jar',
                                                    '--jar', 'emv.jar']),
                            msg='using --jar more than once is illegal')

        with open('forged.jar', 'w') as f:
            f.write('this is a jar')
        os.chmod('forged.jar', S_IRUSR | S_IWUSR | S_IXUSR)

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar', 'fake.jar',
                                                    '--jar', 'forged.jar']),
                            msg='using --jar more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar', 'fake.jar',
                                                    'forged.jar']),
                            msg='--jar must be given a single argument')

        remove_file('forged.jar')
        remove_file('fake.jar')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--jar', 'fake.jar']),
                            msg='--jar must be given an existing file path')

    def test_tool_output(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--toolOutput', 'Griffindor.json']),
                         msg='typical use of --toolOutput')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--toolOutput', 'Slytherin']),
                         msg='--toolOutput files do not require a suffix of .json')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--toolOutput', '.']),
                            msg='--toolOutput argument is a directory, must be a file path')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--toolOutput', '..']),
                            msg='--toolOutput argument is a directory, must be a file path')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--toolOutput', 'Hufflepuff',
                                                    '--toolOutput', 'Ravenclaw']),
                            msg='using --toolOutput more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--toolOutput', 'Hufflepuff',
                                                    '--toolOutput', 'Hufflepuff']),
                            msg='using --toolOutput more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--toolOutput', 'Hufflepuff',
                                                    'Ravenclaw']),
                            msg='--toolOutput must be given only a single argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--toolOutput', 'Hufflepuff',
                                                    'Hufflepuff']),
                            msg='--toolOutput must be given only a single argument')

    def test_path(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--path', '.']),
                         msg='typical use of --path')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--path', '..']),
                         msg='typical use of --path')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--path']),
                            msg='--path must be given an argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--path', 'mexico']),
                            msg='--path argument mexico does not exist')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--path', 'rome.sol']),
                            msg='--path argument rome.sol is a file and not a directory')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--path', '.', '--path', '.']),
                            msg='using --path more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--path', '.', '..']),
                            msg='--path must given only one argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--path', '.', '.']),
                            msg='--path must given only one argument')

    def test_optimize(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '1']),
                         msg='typical use of --optimize')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '534760']),
                         msg='typical use of --optimize')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '0']),
                         msg='Optimizing for zero is allowed')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '-1']),
                            msg='Number of runs must be non-negative')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '-551245']),
                            msg='Number of runs must be non-negative')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '1.0']),
                            msg='Number of runs must be an integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '3e2']),
                            msg='Number of runs must be an integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', 'dolphin']),
                            msg='Number of runs must be an integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize']),
                            msg='--optimize must get an argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '800', '800']),
                            msg='--optimize must get a single argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '800', '--optimize',
                                                    '900']),
                            msg='--optimize cannot be used more than once')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '10',
                                                 "--solc_args", "['--optimize', '--optimize-runs', '10']"]),
                         msg='Using the certoraRun --optimize with the solc arg --optimize is not an error if they '
                             'agree on the value')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '200',
                                                 "--solc_args", "['--optimize']"]),
                         msg='Using the certoraRun --optimize with the solc arg --optimize is not an error if they '
                             'agree on the value')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--optimize', '20',
                                                    "--solc_args", "['--optimize', '--optimize-runs', '10']"]),
                            msg='Using the certoraRun --optimize with the solc arg --optimize with conflicting values')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', "--optimize", "15",
                                                    "--solc_args", "['--optimize-runs', '10']"]),
                            msg='Using the solc arg --optimize-runs without --optimize is an error')

    def test_unique_mode_of_operation(self) -> None:
        """
        Ascertains we have only 1 mode of operation in use.
        The four modes are:
        1. There is a single .tac file
        2. There is a single .conf file
        3. --assert
        4. --verify
        @return:
        """

        with open('tmp.tac', 'w') as f:
            f.write("Rick")

        with open('tmp2.tac', 'w') as f:
            f.write("Morty")

        with open('tmp.conf', 'w') as f:
            f.write('{"files": []}')

        with open('tmp2.conf', 'w') as f:
            f.write('{"files": []}')

        # mode 1
        self.assertEqual(0, self.call_with_args(['tmp.tac']), msg='using mode #1')
        self.assertNotEqual(0, self.call_with_args(['tmp.tac', 'tmp2.tac']), msg='Can use only a single TAC file')

        # mode 2
        self.assertEqual(0, self.call_with_args(['tmp.conf']), msg='using mode #2')
        self.assertNotEqual(0, self.call_with_args(['tmp.conf', 'tmp2.conf']), msg='Can use only a single CONF file')

        # mode 3
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome']), msg='using mode #3')

        # mode 4
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', 'rome:spec.spec']), msg='using mode #4')

        # mode 1 + 2:
        self.assertNotEqual(0, self.call_with_args(['tmp.tac', 'tmp.conf']), msg='using modes #1 and #2')

        # mode 1 + 3:
        self.assertNotEqual(0, self.call_with_args(['tmp.tac', '--assert', 'tmp']), msg='using modes #1 and #3')

        # mode 1 + 4:
        self.assertNotEqual(0, self.call_with_args(['tmp.tac', '--verify', 'tmp:spec.spec']),
                            msg='using modes #1 and #4')

        # mode 2 + 3:
        self.assertNotEqual(0, self.call_with_args(['tmp.conf', '--assert', 'tmp']), msg='using modes #2 and #3')

        # mode 2 + 4:
        self.assertNotEqual(0, self.call_with_args(['tmp.conf', '--verify', 'rome:spec.spec']),
                            msg='using modes #2 and #4')

        # mode 3 + 4:
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--verify', 'rome:spec.spec']),
                            msg='using modes #3 and #4')

        # mode 1 + 2 + 3:
        self.assertNotEqual(0, self.call_with_args(['tmp.tac', 'tmp.conf', '--assert', 'tmp']),
                            msg='using modes #1, #2 and #3')

        # mode 1 + 2 + 4:
        self.assertNotEqual(0, self.call_with_args(['tmp.tac', 'tmp.conf', '--verify', 'tmp:spec.spec']),
                            msg='using modes #1, #2 and #4')

        # mode 1 + 3 + 4:
        self.assertNotEqual(0, self.call_with_args(['tmp.tac', '--assert', 'tmp', '--verify', 'tmp:spec.spec']),
                            msg='using modes #1, #3 and #4')

        # mode 2 + 3 + 4:
        self.assertNotEqual(0, self.call_with_args(['tmp.conf', '--assert', 'tmp', '--verify', 'tmp:spec.spec']),
                            msg='using modes #2, #3 and #4')

        # mode 1 + 2 + 3 + 4:
        self.assertNotEqual(0, self.call_with_args(['tmp.tac', 'tmp.conf', '--assert', 'tmp', '--verify',
                                                    'tmp:spec.spec']),
                            msg='using all 4 modes at once')

        # No mode
        self.assertNotEqual(0, self.call_with_args(['rome.sol']), msg='Must use exactly one mode')

        remove_file('tmp.tac')
        remove_file('tmp2.tac')
        remove_file('tmp.conf')
        remove_file('tmp2.conf')

    def test_packages_args(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages_path', '.']),
                         msg='typical use of --packages_path')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages_path', '..']),
                         msg='typical use of --packages_path')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages_path']),
                            msg='--packages_path must be given an argument')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages_path', '.', '..']),
                            msg='--packages_path must be given a single argument')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages_path', '.',
                                                    '--packages_path', '..']),
                            msg='using --packages_path more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages_path', '.',
                                                    '--packages_path', '.']),
                            msg='using --packages_path more than once is illegal')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages_path', 'KFC']),
                            msg='--packages_path must be given an existing path')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages_path', 'rome.sol']),
                            msg='--packages_path must be given a file, not a directory')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a=.']),
                         msg='typical use of --packages')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a=.', 'b=.', 'c=..']),
                         msg='typical use of --packages with several arguments')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages']),
                            msg='--packages must be given a single argument')

        # test below have bad formatting
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a']),
                            msg='--packages argument has a bad format, should be <name>=<path>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a:b']),
                            msg='--packages argument has a bad format, should be <name>=<path>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a=']),
                            msg='--packages argument has a bad format, should be <name>=<path>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', '=b']),
                            msg='--packages argument has a bad format, should be <name>=<path>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', '=']),
                            msg='--packages argument has a bad format, should be <name>=<path>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a==.']),
                            msg='--packages argument has a bad format, should be <name>=<path>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a=b=.']),
                            msg='--packages argument has a bad format, should be <name>=<path>')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a=b']),
                            msg='--packages argument error: path b does not exist')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a=rome.sol']),
                            msg='--packages argument error: path rome.sol is a file not a directory')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a=.', 'a=..']),
                            msg='--packages argument a was given two contradicting definitions')

        # Double usage of the flag --packages
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--packages', 'a=.', 'b=.',
                                                    '--packages', 'c=..']),
                            msg='using --packages more than once is illegal')

    def test_deployment_args(self) -> None:
        if "CERTORAKEY" in os.environ:
            del os.environ["CERTORAKEY"]
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                         msg='running without a set CERTORAKEY will use the public key by default')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                         msg='running without a set CERTORAKEY will use the public key by default')

        os.environ['CERTORAKEY'] = ""
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                         msg='running without a set CERTORAKEY will use the public key by default')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                         msg='running without a set CERTORAKEY will use the public key by default')

        os.environ['CERTORAKEY'] = "1"
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                            msg='CERTORAKEY is too short')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                            msg='CERTORAKEY is too short')

        os.environ['CERTORAKEY'] = "1" * 31
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                            msg='CERTORAKEY is too short')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                            msg='CERTORAKEY is too short')

        os.environ['CERTORAKEY'] = "1" * 33
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                            msg='CERTORAKEY is too short')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                            msg='CERTORAKEY is too short')

        os.environ['CERTORAKEY'] = "1" * 39
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                            msg='CERTORAKEY is too short')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                            msg='CERTORAKEY is too short')

        os.environ['CERTORAKEY'] = "1" * 41
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                            msg='CERTORAKEY is too long')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                            msg='CERTORAKEY is too long')

        os.environ['CERTORAKEY'] = "@" + "8" * 39
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                            msg='CERTORAKEY has an illegal character')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                            msg='CERTORAKEY has an illegal character')

        os.environ['CERTORAKEY'] = "q" + "8" * 39
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                            msg='CERTORAKEY has an illegal character')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                            msg='CERTORAKEY has an illegal character')

        os.environ['CERTORAKEY'] = "abcdefABCDEF0123456789" + 18 * "0"

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                         msg='typical use of --cloud without an argument')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', 'testing']),
                         msg='typical use of --cloud with an argument')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', 'production']),
                         msg='typical use of --cloud without an argument, in this case the default')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', 'rome']),
                         msg='typical use of --cloud with an argument')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', 'rome.sol']),
                         msg='typical use of --cloud with an argument, any string is legal')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', 'production',
                                                    '--cloud', 'testing']),
                            msg='using --cloud more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', 'debug', 'testing']),
                            msg='--cloud must be given a single argument')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                         msg='typical use of --staging without an argument')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', 'production']),
                         msg='typical use of --staging with an argument, in this case the defualt')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', 'testing']),
                         msg='typical use of --staging with an argument')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', 'rome']),
                         msg='typical use of --staging with an argument')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', 'rome.sol']),
                         msg='typical use of --staging with an argument, the argument string is not checked')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', 'production',
                                                    '--staging', 'testing']),
                            msg='Using the option --staging more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', 'debug', 'testing']),
                            msg='staging must be given a single argument')

        # using both --staging and --cloud is not allowed
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', '--cloud']),
                            msg='--staging and --cloud annot be used together')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', 'a', '--cloud']),
                            msg='--staging and --cloud annot be used together')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', '--cloud', 'a']),
                            msg='--staging and --cloud annot be used together')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', '--staging']),
                            msg='--staging and --cloud annot be used together')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', 'a', '--staging']),
                            msg='--staging and --cloud annot be used together')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', '--staging', 'a']),
                            msg='--staging and --cloud annot be used together')

        # repeating arguments is bad
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', '--cloud']),
                            msg='Using the option --cloud more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud', 'a', '--cloud']),
                            msg='Using the option --cloud more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', '--staging']),
                            msg='Using the option --staging more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', 'a', '--staging']),
                            msg='Using the option --staging more than once is illegal')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--cloud']),
                         msg='old CERTORAKEY length is 32, and it is allowed')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging']),
                         msg='old CERTORAKEY length is 32, and it is allowed')

    def test_java_args(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--javaArgs', '"-ea"']),
                         msg='typical use of --javaArgs')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--javaArgs', '"-s=9"']),
                         msg='typical use of --javaArgs')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--javaArgs',
                                                 '"-Xmx8g -Dcvt.default.parallelism=2"']),
                         msg='typical use of --javaArgs, can have anything inside the double quotes, even spaces')

        # No ""
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--javaArgs', "'-s'"]),
                            msg='--javaArgs must be encapsulated in double quotes, not single quotes')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--javaArgs', "“-s“"]),
                            msg='--javaArgs must be encapsulated in double quotes "", not pretty quotes ““')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--javaArgs', "-s"]),
                            msg='--javaArgs must be encapsulated in double quotes')
        # No args
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--javaArgs']),
                            msg="--javaArgs must be given an argument")
        # empty args
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--javaArgs', "''"]),
                            msg="--javaArgs cannot be given an empty argument")

        # Multiple definition allowed
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--java_args', '"-ea"', '--assert', 'rome',
                                                    '--javaArgs', '"-Xmx8g -Dcvt.default.parallelism=2"']),
                            msg='Using --javaArgs multiples times is allowed')

    def test_settings(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', "-assumeUnwindCond"]),
                         msg='typical use of --settings')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', "-b=3"]),
                         msg='typical use of --settings')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', "-s='robert'"]),
                         msg='typical use of --settings, quotes are legal')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', '-m="foo(type,type)"']),
                         msg='--settings with parenthesis')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                                 '-m="foo(type,type,(type,type))"']),
                         msg='--settings with nested parenthesis')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                                 "-assumeUnwindCond,-q=3,-k='fun'"]),
                         msg='typical use of --settings, multiple flags separated by commas')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                                 "-s=9,-k='pizza',-q"]),
                         msg='typical use of --settings, multiple flags separated by commas')

        # # Multiple definition is ALLOWED
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', "-s",
                                                 '--settings', "-f"]),
                         msg='using --settings several times is allowed')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', "-assumeUnwindCond",
                                                 "--cache", "treasure", "--settings", "-b=3"]),
                         msg='using --settings several times is allowed')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', "'-s'"]),
                            msg='--settings arguments cannot be wrapped in single quotes')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', "s=9"]),
                            msg='--settings arguments must be options starting with a dash, s is without a dash')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', "-k,s=9"]),
                            msg='--settings arguments must be options starting with a dash, s is without a dash')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings']),
                            msg='--settings must be given an argument')

        # Pretty quotes are illegal
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', '-m=“foo(type)“']),
                            msg='using pretty quotes ““ is illegal, only "" quotes are legal')

    def test_address(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome:1"]),
                         msg='typical use of --address')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome:0"]),
                         msg='typical use of --address, slot 0 is legal')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome:99999"]),
                         msg='typical use of --address')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol:md', '--assert', 'rome', '--address',
                                                 "rome:2", "md:2"]),
                         msg='--address accepts many arguments')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome:1", "rome:1"]),
                         msg='defining the same address multiple times is redundant, but legal')

        # not a contract
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome.sol:1"]),
                            msg='--address wrong argument: Undefined contract name rome.sol')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "madrid:1"]),
                            msg='--address wrong argument: Undefined contract name madrid')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', ":1"]),
                            msg='--address wrong argument: No contract name given')

        # illegal number
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome:-1"]),
                            msg='--address wrong argument: slot number cannot be negative')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome:"]),
                            msg='--address wrong argument: Must be of form <contract>:<non-negative integer>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome"]),
                            msg='--address wrong argument: Must be of form <contract>:<non-negative integer>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "."]),
                            msg='--address wrong argument: Must be of form <contract>:<non-negative integer>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome:rome"]),
                            msg='--address wrong argument: Must be of form <contract>:<non-negative integer>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address', "rome:italy"]),
                            msg='--address wrong argument: Must be of form <contract>:<non-negative integer>')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--address']),
                            msg='--address must be given an argument')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', 'madrid.sol:md', '--assert', 'rome', '--address',
                                                    "rome:2", "--address", "md:2"]),
                            msg='Using the option --address more than once is illegal')

        with open('Bobby.tac', 'w') as f:
            f.write('Fisher')
        self.assertNotEqual(0, self.call_with_args(['Bobby.tac', '--address', "Bobby:1"]),
                            msg='--address cannot be used with a .tac file')
        remove_file('Bobby.tac')

        with open('Kuala.conf', 'w') as f:
            f.write('Lumpur')
        self.assertNotEqual(0, self.call_with_args(['Kuala.conf', '--address', "Kuala:1"]),
                            msg='--address cannot be used with a .conf file')
        remove_file('Kuala.conf')

    def test_debug(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--debug']),
                         msg='typical use of --debug')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--debug', '--debug']),
                         msg='using --debug more than once is redundant, but not an error')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--debug', '5']),
                         msg='--debug can receive topics, even nonsense ones')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--debug', 'rome']),
                         msg='--debug can receive topics names')

    def test_debug_topics(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--debug', '--debug_topics']),
                         msg='typical use of --debug_topics')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--debug_topics']),
                            msg='--debug_topics must be used with --debug')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--debug', '--debug_topics', '5']),
                            msg='--debug_topics does not receive arguments')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--debug', '--debug_topics',
                                                 '--debug_topics']),
                         msg='--debug_topics can be used twice, it just has no effect')

    def test_no_compare(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--no_compare']),
                         msg='typical use of --no_compare')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--no_compare', '--no_compare']),
                         msg='using --no_compare more than once is redundant, but not an error')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--no_compare', '5']),
                            msg='--no_compare cannot be given arguments')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--no_compare', 'rome']),
                            msg='--no_compare cannot be given arguments')

    def test_expected_file(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--expected_file', 'exp.json']),
                         msg='typical use of --expected_file')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--expected_file']),
                            msg='using --expected_file without arguments is illegal')

        self.assertNotEqual(0,
                            self.call_with_args(
                                ['rome.sol', '--assert', 'rome', '--expected_file', 'exp.json', 'rome']),
                            msg='--expected_file cannot be given multiple arguments')

        mydir_name = 'mydir'
        mydir = Path.cwd() / mydir_name
        if not mydir.exists():
            mydir.mkdir()

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--expected_file', mydir_name]),
                            msg='--expected_file cannot be given a directory')

    def test_send_only(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--send_only']),
                         msg='typical use of --send_only')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--send_only', '--send_only']),
                         msg='using --send_only more than once is redundant, but not an error')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--send_only', '5']),
                            msg='--send_only cannot be given arguments')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--send_only', 'rome']),
                            msg='--send_only cannot be given arguments')

    def test_struct_link(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0=rome']),
                         msg='typical use of --structLink')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0xc=rome']),
                         msg='--structLink accepts slot as hexadecimal numbers')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0XC=rome']),
                         msg='--structLink accepts slot as hexadecimal numbers')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0X1c=rome']),
                         msg='--structLink accepts slot as hexadecimal numbers')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0x1C=rome']),
                         msg='--structLink accepts slot as hexadecimal numbers')
        self.assertEqual(0, self.call_with_args(['rome.sol', 'madrid.sol', '--assert', 'rome', '--structLink',
                                                 'rome:1=madrid', 'rome:2=madrid', 'rome:1009=rome']),
                         msg='--structLink can have many arguments')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', 'madrid.sol', '--assert', 'rome', '--structLink',
                                                    'rome:1=madrid', '--structLink', 'rome:2=madrid', 'rome:19=rome']),
                            msg='Using the option --structLink more than once is illegal')

        # undefined contract names
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'madrid:0=rome']),
                            msg='Illegal --structLink argument: undefined contract name madrid')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0=madrid']),
                            msg='Illegal --structLink argument: undefined contract name madrid')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'a:0=b']),
                            msg='Illegal --structLink argument: undefined contract names: a, b')

        # bad format
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0=']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:=rome']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome=rome']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', '0=rome']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', ':0=rome']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0=']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:=']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', ':=rome']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', ':12=']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', ':=']),
                            msg='Illegal --structLink argument format. Should be <contract>:<number>=<contract>')

        # bad int format
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:-1=rome']),
                            msg='Illegal --structLink slot number cannot be negative')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:-567=rome']),
                            msg='Illegal --structLink slot number cannot be negative')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:1.0=rome']),
                            msg='Illegal --structLink slot number must be an integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0.1=rome']),
                            msg='Illegal --structLink slot number must be an integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:e-5=rome']),
                            msg='Illegal --structLink slot number must be an integer')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:c=rome']),
                         msg='Illegal --structLink slot number must be an integer')

        # no argument
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink']),
                            msg='--structLink must be given an argument')

        # double use of --struct link
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0=rome',
                                                    '--structLink', 'rome:10=rome']),
                            msg='Using the option --structLink more than once is illegal')

        # link duplication
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--structLink', 'rome:0=rome',
                                                 'rome:0=rome']),
                         msg='The same link definition more than once is redundant, but legal')

        # contradicting link definition
        self.assertNotEqual(0, self.call_with_args(['rome.sol', 'madrid.sol', '--assert', 'rome', '--structLink',
                                                    'rome:0=rome', 'rome:0=madrid']),
                            msg='The same slot at the same contract has contradicting definitions')

        with open('Obi.tac', 'w') as f:
            f.write('One Kenobi')

        self.assertNotEqual(0, self.call_with_args(['Obi.tac', '--structLink', 'Obi:0=Obi']),
                            msg='cannot use --structLink with a .tac file')
        remove_file('Obi.tac')

        with open('Lou.conf', 'w') as f:
            f.write('Reed')

        self.assertNotEqual(0, self.call_with_args(['Lou.conf', '--structLink', 'Lou:0=Lou']),
                            msg='cannot use --structLink with a .conf file')
        remove_file('Lou.conf')

    def test_build_only(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--build_only']),
                         msg='correct use of --build_only')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--build_only',
                                                    'rome']),
                            msg='--build_only cannot be given an argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--build_only', '1']),
                            msg='--build_only cannot be given an argument')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--build_only',
                                                 '--build_only']),
                         msg='using --build_only twice is redundant, but is not a mistake')

    def test_typecheck_only(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--staging', '--typecheck_only']),
                         msg='correct use of --typecheck_only')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--typecheck_only',
                                                    '--jar', 'fake.jar']),
                            msg='incorrect use of --typecheck_only - must be remote mode')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--typecheck_only',
                                                    'rome']),
                            msg='--typecheck_only cannot be given an argument')
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--typecheck_only', '1']),
                            msg='--typecheck_only cannot be given an argument')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--typecheck_only',
                                                 '--cloud', '--typecheck_only']),
                         msg='using --typecheck_only twice is redundant, but is not a mistake')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--typecheck_only',
                                                    '--disableLocalTypeChecking']),
                            msg='using --typecheck_only together with --disableLocalTypeChecking is disallowed')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--typecheck_only',
                                                    '--build_only']),
                            msg='using --typecheck_only together with --build_only is disallowed')

    def test_disable_local_type_checking(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--disableLocalTypeChecking']),
                         msg='correct use of --disableLocalTypeChecking')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--disableLocalTypeChecking',
                                                    'rome']),
                            msg='--disableLocalTypeChecking cannot be given an argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--disableLocalTypeChecking', '1']),
                            msg='--disableLocalTypeChecking cannot be given an argument')

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--disableLocalTypeChecking',
                                                 '--disableLocalTypeChecking']),
                         msg='using --disableLocalTypeChecking twice is redundant, but is not a mistake')

    def test_queue_wait_minutes(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '1']),
                         msg='correct use of --queue_wait_minutes')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '0']),
                         msg='--queue_wait_minutes accepts the argument zero')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '234566']),
                         msg='correct use of --queue_wait_minutes')

        # Bad number formats
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', 'rome']),
                            msg='--queue_wait_minutes must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '-1']),
                            msg='--queue_wait_minutes must be given a non-negative integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '-1234']),
                            msg='--queue_wait_minutes must be given a non-negative integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '0.1']),
                            msg='--queue_wait_minutes must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '1.000']),
                            msg='--queue_wait_minutes must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '0x1']),
                            msg='--queue_wait_minutes must be given a decimal integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '0X1c']),
                            msg='--queue_wait_minutes must be given a decimal integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '2e-9']),
                            msg='--queue_wait_minutes must be given an integer argument')

        # No arguments
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes']),
                            msg='--queue_wait_minutes must be given an argument')

        # Double use of flag
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '1',
                                                    '--queue_wait_minutes', '2']),
                            msg='Using the option --queue_wait_minutes more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--queue_wait_minutes', '1',
                                                    '--queue_wait_minutes', '1']),
                            msg='Using the option --queue_wait_minutes more than once is illegal')

    def test_max_poll_minutes(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '1']),
                         msg='correct use of --max_poll_minutes')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '0']),
                         msg='--max_poll_minutes accepts the argument zero')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '234566']),
                         msg='correct use of --max_poll_minutes')

        # Bad number formats
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', 'rome']),
                            msg='--max_poll_minutes must be given a non-negative integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '-1']),
                            msg='--max_poll_minutes must be given a non-negative integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '-1234']),
                            msg='--max_poll_minutes must be given a non-negative integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '0.1']),
                            msg='--max_poll_minutes must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '1.000']),
                            msg='--max_poll_minutes must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '0x1']),
                            msg='--max_poll_minutes must be given a decimal integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '0X1c']),
                            msg='--max_poll_minutes must be given a decimal integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '2e-9']),
                            msg='--max_poll_minutes must be given an integer argument')

        # No arguments
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes']),
                            msg='--max_poll_minutes must be given an argument')

        # Double use of flag
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '1',
                                                    '--max_poll_minutes', '2']),
                            msg='Using the option --max_poll_minutes more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_poll_minutes', '1',
                                                    '--max_poll_minutes', '1']),
                            msg='Using the option --max_poll_minutes more than once is illegal')

    def test_log_query_frequency_seconds(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds', '1']),
                         msg='correct use of --log_query_frequency_seconds')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds', '0']),
                         msg='--log_query_frequency_seconds accept the argument zero')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                 '234566']),
                         msg='correct use of --log_query_frequency_seconds')

        # Bad number formats
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    'rome']),
                            msg='--log_query_frequency_seconds must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    '-1']),
                            msg='--log_query_frequency_seconds must be given a non-negative argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    '-1234']),
                            msg='--log_query_frequency_seconds must be given a non-negative argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    '0.1']),
                            msg='--log_query_frequency_seconds must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    '1.000']),
                            msg='--log_query_frequency_seconds must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    '0x1']),
                            msg='--log_query_frequency_seconds must be given a decimal integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    '0X1c']),
                            msg='--log_query_frequency_seconds must be given a decimal integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    '2e-9']),
                            msg='--log_query_frequency_seconds must be given an integer argument')

        # No arguments
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds']),
                            msg='--log_query_frequency_seconds must be given an argument')

        # Double use of flag
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    '1', '--log_query_frequency_seconds', '2']),
                            msg='Using the option --log_query_frequency_seconds more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--log_query_frequency_seconds',
                                                    '1', '--log_query_frequency_seconds', '1']),
                            msg='Using the option --log_query_frequency_seconds more than once is illegal')

    def test_max_attempts_to_fetch_output(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                 '1']),
                         msg='correct use of --max_attempts_to_fetch_output')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                 '0']),
                         msg='--max_attempts_to_fetch_output can be given an input of 0')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                 '234566']),
                         msg='correct use of --max_attempts_to_fetch_output')

        # Bad number formats
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    'rome']),
                            msg='Using the option --max_attempts_to_fetch_output must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    '-1']),
                            msg='Using the option --max_attempts_to_fetch_output must be given a non-negative integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    '-1234']),
                            msg='Using the option --max_attempts_to_fetch_output must be given a non-negative integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    '0.1']),
                            msg='Using the option --max_attempts_to_fetch_output must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    '1.000']),
                            msg='Using the option --max_attempts_to_fetch_output must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    '0x1']),
                            msg='Using the option --max_attempts_to_fetch_output must be given a decimal integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    '0X1f']),
                            msg='Using the option --max_attempts_to_fetch_output must be given a decimal integer')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    '2e-9']),
                            msg='Using the option --max_attempts_to_fetch_output must be given an integer argument')

        # No arguments
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output']),
                            msg='--max_attempts_to_fetch_output must be given an argument')

        # Double use of flag
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    '1', '--max_attempts_to_fetch_output', '2']),
                            msg='Using the option --max_attempts_to_fetch_output more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_attempts_to_fetch_output',
                                                    '1', '--max_attempts_to_fetch_output', '1']),
                            msg='Using the option --max_attempts_to_fetch_output more than once is illegal')

    def test_delay_fetch_output_seconds(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds', '1']),
                         msg='correct use of --delay_fetch_output_seconds')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds', '0']),
                         msg='--delay_fetch_output_seconds can be given an input of 0')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                 '234566']),
                         msg='correct use of --delay_fetch_output_seconds')

        # Bad number formats
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    'rome']),
                            msg='--delay_fetch_output_seconds must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    '-1']),
                            msg='--delay_fetch_output_seconds must be given a non-negative integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    '-1234']),
                            msg='--delay_fetch_output_seconds must be given a non-negative integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    '0.1']),
                            msg='--delay_fetch_output_seconds must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    '1.000']),
                            msg='--delay_fetch_output_seconds must be given an integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    '0x1']),
                            msg='--delay_fetch_output_seconds must be given a decimal integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    '0X1f']),
                            msg='--delay_fetch_output_seconds must be given a decimal integer argument')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    '2e-9']),
                            msg='--delay_fetch_output_seconds must be given an integer argument')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds']),
                            msg='--delay_fetch_output_seconds must be given an argument')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    '1', '--delay_fetch_output_seconds', '2']),
                            msg='Using the option --delay_fetch_output_seconds more than once is illegal')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--delay_fetch_output_seconds',
                                                    '1', '--delay_fetch_output_seconds', '1']),
                            msg='Using the option --delay_fetch_output_seconds more than once is illegal')

    def test_msg(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--msg', '1']),
                         msg="option --msg accepts ANY string")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--msg', 'cup']),
                         msg="option --msg accepts ANY string")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--msg', '"rio de janeiro"']),
                         msg="option --msg accepts ANY string")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--msg', 'rio de janeiro']),
                         msg="option --msg accepts ANY string")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--msg']),
                            msg="--msg must be given an argument")
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--msg', '--cache', 'teeth']),
                            msg="--msg must be given an argument")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--msg', 'cup', 'cake']),
                            msg="Too many arguments for the option --msg, only one expected")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--msg', 'cup', '--msg', 'cake']),
                            msg="Using the option --msg more than once is illegal")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--msg', '“rio de janeiro“']),
                            msg="pretty quote character “ is illegal")

    def test_process(self) -> None:
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--process', 'verify']),
                         msg="option --process accepts ANY string")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--process', '12']),
                         msg="option --process accepts ANY string")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--process', 'emv']),
                         msg="option --process accepts ANY string, including the default")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--process']),
                            msg="option --process must be given an argument")
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--process', 'a', 'b']),
                            msg="option --process must be given a single argument")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--process', 'a', '--process', 'b']),
                            msg="option --process cannot be used more than once")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--process', 'a', '--process', 'a']),
                            msg="option --process cannot be used more than once")

    def test_rule(self) -> None:
        '''
        We depend in this test on Test/RulePickingTest/choose_rules.spec.
        It contains two rules (always_true and always_false) and an invariant (i_small)
        '''
        if is_ci_or_git_action():
            spec_file = "Test/RulePickingTest/choose_rules.spec"
        else:
            spec_file = "../../Test/RulePickingTest/choose_rules.spec"

        # Checking whether the rule exists in the spec file is done at the jar, not Python

        # testing --rule
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--rule', 'always_true']),
                         msg="typical use of --rule")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--rule',
                                                 'always_false']),
                         msg="typical use of --rule")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--rule', 'tautology']),
                         msg="--rule also accept invariant names")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--rule']),
                            msg="--rule without an argument")
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--rule',
                                                    'always_true', 'always_false']),
                            msg="--rule without two arguments")

        # testing --settings -rule
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                 '-rule=always_true']),
                         msg="typical use of --settings -rule")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                 '-rule=always_false']),
                         msg="typical use of --settings -rule")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                 '-rule=tautology']),
                         msg="--settings -rule can get an invariant too")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                    '-rule']), msg="no rule name")
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                    '-rule=']), msg="empty rule name")
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                    '-rule==']), msg="empty rule name")
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                    '-rule=a=b']), msg="malformed rule name")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                    '-rule=always_true', '-rule=always_false']),
                            msg='only one rule can be verified at a time by -rule')
        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                 '-rule=always_true,-rule=always_true']),
                         msg='Specifying the same rule twice is highly discouraged, but not an error')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--settings',
                                                    '-rule=always_true', '--settings', '-rule=always_false']),
                            msg="two different rule names")

        # testing --rule AND --settings -rule

        self.assertEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--rule', 'always_true',
                                                 '--settings', '-rule=always_true']),
                         msg='Specifying the same rule twice is highly discouraged, but not an error')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--verify', f'rome:{spec_file}', '--rule',
                                                    'always_true', '--settings', '-rule=always_false']),
                            msg='Specifying two different rules')

        # --rule can only be used with --verify mode
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--rule', 'always_true']),
                            msg="--rule cannot be used in assert mode")

        with open('tmp.tac', 'w') as f:
            f.write("don't mess with Texas")
        self.assertNotEqual(0, self.call_with_args(['tmp.tac', '--rule', 'always_true']),
                            msg="--rule cannot be used in TAC mode")
        remove_file('tmp.tac')

    def __test_single_val_dual_args(self, arg_name: str, setting_name: str, first_val: Any, second_val: Any,
                                    allow_zero: bool = False) -> None:
        """
        allow_zero set to true means the flag we check can also take 0 arguments, so it will adapt accordingly
        for tests that test 0 arguments given.
        """
        assert first_val != second_val, f"wrong use of test: given two identical values {first_val}"

        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', first_val]),
                         msg=f"typical use of --{arg_name} with value {first_val}")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', second_val]),
                         msg=f"typical use of --{arg_name} with value {second_val}")

        if allow_zero:
            self.assertEqual(0,
                             self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}']),
                             msg=f"--{arg_name} may not get a value")
        else:
            self.assertNotEqual(0,
                                self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}']),
                                msg=f"--{arg_name} must get a value")

        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', first_val,
                                                 second_val]),
                            msg=f"--{arg_name} must get a single value, got two instead")

        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                              f'-{setting_name}={first_val}']),
                         msg=f"typical use of --settings -{setting_name} with value {first_val}")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                              f'-{setting_name}={second_val}']),
                         msg=f"typical use of --settings -{setting_name} with value {second_val}")

        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', first_val,
                                                 f'--{arg_name}', second_val]),
                            msg=f"conflicting values for --{arg_name}: {first_val} and {second_val}")

        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                              f'-{setting_name}={first_val},-{setting_name}={first_val}']),
                         msg=f"using --settings -{setting_name} twice with the same value is redundant, "
                             f"but not an error")

        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                                 f'-{setting_name}', first_val, f'-{setting_name}', second_val]),
                            msg=f"conflicting values for --settings -{setting_name}: {first_val} and {second_val}")

        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                              f'-{setting_name}={first_val}', f'--{arg_name}', first_val]),
                         msg=f"using --settings -{setting_name} and --{arg_name} with the same value is redundant, "
                             f"but not an error")

        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                                 f'-{setting_name}={first_val}', f'--{arg_name}', second_val]),
                            msg=f"using --settings -{setting_name} and --{arg_name} with conflicting values")

        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                                 f'-{setting_name}={second_val}', f'--{arg_name}', first_val]),
                            msg=f"using --settings -{setting_name} and --{arg_name} with conflicting values")

    def __test_implicit_bool_dual_args(self, arg_name: str, setting_name: str) -> None:
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}']),
                         msg=f"typical use of --{arg_name}")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', 'fake_value']),
                            msg=f"--{arg_name} cannot get a value")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', '12']),
                            msg=f"--{arg_name} cannot get a value")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', f'--{arg_name}']),
                         msg=f"Using --{arg_name} more than once is redundant, but not an error")

        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}']),
                         msg=f"typical use of --settings -{setting_name}")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}=1']),
                            msg=f"--settings -{setting_name} cannot get a value")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}=a']),
                            msg=f"--settings -{setting_name} cannot get a value")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                              f'-{setting_name},-{setting_name}']),
                         msg=f"using --settings -{setting_name} twice with the same value is redundant, "
                             f"but not an error")

        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}',
                                              f'--{arg_name}']),
                         msg=f"using both --{arg_name} and --settings -{setting_name} is redundant but not an error")

    def __test_explicit_bool_dual_args(self, arg_name: str, setting_name: str) -> None:
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}']),
                         msg=f"typical use of --{arg_name}")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', 'fake_value']),
                            msg=f"--{arg_name} cannot get a value")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', '12']),
                            msg=f"--{arg_name} cannot get a value")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', f'--{arg_name}', f'--{arg_name}']),
                         msg=f"Using --{arg_name} more than once is redundant, but not an error")

        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}=true']),
                         msg=f"typical use of --settings -{setting_name}=true")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}=false']),
                         msg=f"--settings -{setting_name}=false is redundant, but not an error")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}=1']),
                            msg=f"--settings -{setting_name} cannot get a non-boolean value")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}=a']),
                            msg=f"--settings -{setting_name} cannot get a non-boolean value")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                              f'-{setting_name}=true,-{setting_name}=true']),
                         msg=f"using --settings -{setting_name} twice with the same truth value is redundant, "
                             f"but not an error")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                              f'-{setting_name}=false,-{setting_name}=false']),
                         msg=f"using --settings -{setting_name} twice with the same truth value is redundant, "
                             f"but not an error")

        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                                 f'-{setting_name}=false,-{setting_name}=true']),
                            msg=f"using --settings -{setting_name} twice with conflicting truth values")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings',
                                                 f'-{setting_name}=true,-{setting_name}=false']),
                            msg=f"using --settings -{setting_name} twice with conflicting truth values")

        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}=true',
                                              f'--{arg_name}']),
                         msg=f"using both --{arg_name} and --settings -{setting_name}=true is redundant "
                             f"but not an error")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', f'-{setting_name}=false',
                                                 f'--{arg_name}']),
                            msg=f"using both --{arg_name} and --settings -{setting_name}=false is a conflict")

    def test_method(self) -> None:
        # This test does not build, so we do not check for the correctness of method, just for conflicts with
        # --settings -m and --method
        self.__test_single_val_dual_args("method", "method", "foo(int,address)", "bar(bool,uint256)")
        self.__test_single_val_dual_args("method", "method", "foo(int,(address,bool))",
                                         "bar((bool,(address,address)),uint256)")

        # We build for the rest of the test

        sol_file = "Test/Method/MethodChoice.sol"

        # testing --method with building. For some reason, CI fails when we try to run and build with correct arguments,
        # so we only check failures

        # failures are quick

        # first round - --assert
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'foo(uint256 a)']),
                            msg="malformed --method, has a variable name")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'foo(uint128 a)']),
                            msg="malformed --method, wrong uint type")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'foo(bool,)']),
                            msg="malformed --method, extra comma")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'foo(,bool)']),
                            msg="malformed --method, extra comma")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'foo(,)']),
                            msg="malformed --method, extra comma")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'secret()']),
                            msg="malformed --method, internal function")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'hidden()']),
                            msg="malformed --method, private function")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'empty_struct(())']),
                            msg="cannot have an empty struct in a method declaration")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'empty_struct(bool, (bool, ()))']),
                            msg="cannot have an empty struct in a method declaration")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'malformed(bool (address), address)']),
                            msg="missing comma before a struct")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--assert', 'MethodChoice', '--method',
                                                         'malformed(bool, (address) address)']),
                            msg="missing comma after a struct")

        # second round - --verify
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'foo(uint256 a)']),
                            msg="malformed --method, has a variable name")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'foo(uint128 a)']),
                            msg="malformed --method, wrong uint type")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'foo(bool,)']),
                            msg="malformed --method, extra comma")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'foo(,bool)']),
                            msg="malformed --method, extra comma")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'foo(,)']),
                            msg="malformed --method, extra comma")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'secret()']),
                            msg="malformed --method, internal function")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'hidden()']),
                            msg="malformed --method, private function")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'empty_struct(())']),
                            msg="cannot have an empty struct in a method declaration")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'empty_struct(bool, (bool, ()))']),
                            msg="cannot have an empty struct in a method declaration")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'malformed(bool (address), address)']),
                            msg="missing comma before a struct")
        self.assertNotEqual(0,
                            self.call_and_run_with_args([f'{sol_file}', '--verify', 'spec.spec', 'MethodChoice',
                                                         '--method', 'malformed(bool, (address) address)']),
                            msg="missing comma after a struct")

    def test_loop_iter(self) -> None:
        self.__test_single_val_dual_args("loop_iter", "b", '1', '2')
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--loop_iter', '1000']),
                         msg="--loop_iter with a large value")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--loop_iter', '0']),
                         msg="--loop_iter with a zero")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--loop_iter', '-1']),
                            msg="--loop_iter with a negative value")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--loop_iter', 'one']),
                            msg="--loop_iter with a string value")
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--settings', '-build=one']),
                         msg="-b is not -build and should pass")

    def test_rule_sanity(self) -> None:
        self.__test_single_val_dual_args("rule_sanity", "ruleSanityChecks", 'basic', 'none', True)
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--rule_sanity',
                                                    'non']), msg="Illegal value for --rule_sanity")

    def test_smt_timeout(self) -> None:
        self.__test_single_val_dual_args("smt_timeout", "t", '100', '1200')
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--smt_timeout', '100000']),
                         msg="--smt_timeout with a large value")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--smt_timeout', '0']),
                            msg="--smt_timeout must be positive")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--smt_timeout', '-1']),
                            msg="--smt_timeout with a negative value")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--smt_timeout', 'one']),
                            msg="--smt_timeout with a string value")

    def test_multi_assert(self) -> None:
        self.__test_implicit_bool_dual_args('multi_assert_check', 'multiAssertCheck')

    def test_unwind_loops(self) -> None:
        self.__test_implicit_bool_dual_args('optimistic_loop', 'assumeUnwindCond')

    def test_short_output(self) -> None:
        self.__test_explicit_bool_dual_args('short_output', 'ciMode')

    def test_max_graph_depth(self) -> None:
        self.__test_single_val_dual_args("max_graph_depth", "graphDrawLimit", '10', '20')
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--max_graph_depth', '10000']),
                         msg="--max_graph_depth with a large value")
        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--max_graph_depth', '0']),
                         msg="--max_graph_depth can be zero")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--max_graph_depth', '-1']),
                            msg="--max_graph_depth with a negative value")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--max_graph_depth', 'one']),
                            msg="--max_graph_depth with a string value")

    def test_log_branch(self) -> None:
        self.assertEqual(0,
                         self.call_with_args(['rome.sol', '--assert', 'rome', '--log_branch', 'certora-log/whatever']),
                         msg="--log_branch can take a value")
        self.assertNotEqual(0,
                            self.call_with_args(['rome.sol', '--assert', 'rome', '--log_branch']),
                            msg="--log_branch must take a value")

    def test_internal_funcs(self) -> None:
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--internal_funcs']),
                            msg='--internal_funcs must get a file')
        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--internal_funcs', 'unreal.json']),
                            msg='--internal_funcs must get an existing file path')

        with open('tmp.json', 'w') as f:
            json.dump({"a": "b"}, f)

        self.assertEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--internal_funcs', 'tmp.json']),
                         msg='typical use of --internal_funcs')

        with open('tmp.txt', 'w') as f:
            json.dump({"a": "b"}, f)

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--internal_funcs', 'tmp.txt']),
                            msg='--internal_funcs is not of type json')

        remove_file('tmp.txt')

        with open('fake.json', 'w') as f:
            f.write("not a json file format")

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--internal_funcs', 'fake.json']),
                            msg='--internal_funcs has an illegal json file format')

        remove_file('fake.json')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--internal_funcs', 'tmp.json',
                                                    'tmp.json']),
                            msg='--internal_funcs got two arguments')

        self.assertNotEqual(0, self.call_with_args(['rome.sol', '--assert', 'rome', '--internal_funcs', 'tmp.json',
                                                    '--internal_funcs', 'tmp.json']),
                            msg='--internal_funcs can only be used once')

        remove_file('tmp.json')

    def test_compiler_warning(self) -> None:
        """
        First check missing return statement warning (more warnings to be added later,
        including generalization of test code)
        """
        sol_file = 'c.sol'
        with open(sol_file, 'w') as f:
            f.write("contract c { function foo() public returns (uint) { 0; } }")

        # The relevant warning code was added in solc7 and up
        self.assertEqual(1,
                         self.call_and_run_with_args([sol_file, '--assert', 'c'], True, "solc7.5"),
                         msg="""an erroneous solidity file (missing return statement)
                         that should fail despite solc emitting only a warning""")

        remove_file(sol_file)

    def test_bytecode(self) -> None:
        """
        Check that --bytecode only works with no files, and not in conjunction to any other mode
        """
        json_file = 'example.json'
        with open(json_file, 'w') as f:
            f.write("{}")
        sol_file = 'c.sol'
        with open(sol_file, 'w') as f:
            f.write("contract c { }")
        spec_file = 'c.spec'
        with open(spec_file, 'w') as f:
            f.write("")

        self.assertEqual(0,
                         self.call_with_args(['--bytecode', json_file, '--bytecode_spec', spec_file], False),
                         msg="""providing bytecode jsons with spec is fine""")

        self.assertNotEqual(0,
                            self.call_with_args(['--bytecode', json_file], False),
                            msg="""providing bytecode jsons only is wrong - need to give spec""")

        self.assertNotEqual(0,
                            self.call_with_args(['--bytecode_spec', spec_file], False),
                            msg="""providing bytecode spec only is wrong - need to give bytecode jsons too""")

        self.assertNotEqual(0,
                            self.call_with_args([sol_file, '--assert', 'c', '--bytecode_spec', spec_file],
                                                False),
                            msg="""providing bytecode spec is disallowed in other modes""")

        self.assertNotEqual(0,
                            self.call_with_args(['--bytecode', '--bytecode_spec', spec_file], False),
                            msg="""providing no bytecode json is disallowed""")

        self.assertEqual(0,
                         self.call_with_args(
                             ['--bytecode', json_file, json_file, '--bytecode_spec', spec_file], False),
                         msg="""providing more than one bytecode json is fine""")

        self.assertNotEqual(0,
                            self.call_with_args(
                                [sol_file, '--bytecode', json_file, '--bytecode_spec', spec_file], False),
                            msg="""providing bytecode json together with any other file is disallowed""")

        self.assertNotEqual(0,
                            self.call_with_args([sol_file, '--bytecode', json_file, '--assert', 'c'], False),
                            msg="""providing bytecode json together with any other file is disallowed""")

        remove_file(json_file)
        remove_file(sol_file)
        remove_file(spec_file)


if __name__ == '__main__':
    unittest.main()
