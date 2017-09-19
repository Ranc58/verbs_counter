import argparse
import os
import shutil
from io import StringIO
from unittest import TestCase
from unittest.mock import patch
from verb_counter.verb_counter import output_to_cli


class TestInfoOutputToCli(TestCase):
    def setUp(self):
        os.mkdir('django')
        os.mkdir('flask')
        os.mkdir('myproject')
        os.mkdir('myproject/myproject2')
        test_verb_func_1 = 'def get_data():\n    pass'
        test_verb_func_2 = 'def give_content():\n    pass'
        test_not_verb_func_1 = 'def check_data():\n    pass'
        test_not_verb_func_2 = 'def output_content():\n    pass'
        with open('django/app_file1.py', 'w') as file1:
            file1.write(test_verb_func_1 + '\n' + test_not_verb_func_1)
        with open('flask/app_file2.py', 'w') as file1:
            file1.write(test_verb_func_2 + '\n' + test_not_verb_func_2)
        with open('flask/info.txt', 'w') as file1:
            file1.write('this is joke file ha-ha-ha')
        with open('myproject/myproject2/app_file3.py', 'w') as file1:
            file1.write(test_verb_func_1 + '\n' + test_not_verb_func_2)
        with open('myproject/app_file3.py', 'w') as file1:
            file1.write(test_verb_func_2 + '\n' + test_not_verb_func_1)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=False, all_names=False))
    def test_verbs_in_default_projects(self, mock_args):
        expected_result = 'dirpath: ./django:\n' \
                          'total ".py" files count: 1\n' \
                          'verb "get" count: 1\n' \
                          '------------\n' \
                          'dirpath: ./flask:\n' \
                          'total ".py" files count: 1\n' \
                          'verb "give" count: 1\n' \
                          '------------\n' \
                          'total verbs: 2\n' \
                          'unique verbs: 2\n' \
                          '"get" in 1 projects\n' \
                          '"give" in 1 projects\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            output_to_cli()
            self.assertEqual(fake_out.getvalue(), expected_result)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=False, all_names=True))
    def test_all_funcs_names_in_default_projects(self, mock_args):
        expected_result = 'dirpath: ./django:\n' \
                          'total ".py" files count: 1\n' \
                          'All funcs names:\n' \
                          '"get_data"\n' \
                          '"check_data"\n' \
                          'verb "get" count: 1\n' \
                          '------------\n' \
                          'dirpath: ./flask:\n' \
                          'total ".py" files count: 1\n' \
                          'All funcs names:\n' \
                          '"give_content"\n' \
                          '"output_content"\n' \
                          'verb "give" count: 1\n' \
                          '------------\n' \
                          'total funcs names: 4\n' \
                          'unique funcs names: 4\n' \
                          'total verbs: 2\n' \
                          'unique verbs: 2\n' \
                          '"get" in 1 projects\n' \
                          '"give" in 1 projects\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            output_to_cli()
            self.assertEqual(fake_out.getvalue(), expected_result)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=['myproject'], all_names=False))
    def test_with_user_projects(self, mock_args):
        expected_result = 'dirpath: ./myproject:\n' \
                          'total ".py" files count: 2\n' \
                          'verb "give" count: 1\n' \
                          'verb "get" count: 1\n' \
                          '------------\n' \
                          'dirpath: ./django:\n' \
                          'total ".py" files count: 1\n' \
                          'verb "get" count: 1\n' \
                          '------------\n' \
                          'dirpath: ./flask:\n' \
                          'total ".py" files count: 1\n' \
                          'verb "give" count: 1\n' \
                          '------------\n' \
                          'total verbs: 4\n' \
                          'unique verbs: 2\n' \
                          '"give" in 2 projects\n' \
                          '"get" in 2 projects\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            output_to_cli()
            self.assertEqual(fake_out.getvalue(), expected_result)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=['myproject'], all_names=True))
    def test_all_funcs_names_with_user_projects(self, mock_args):
        expected_result = 'dirpath: ./myproject:\n' \
                          'total ".py" files count: 2\n' \
                          'All funcs names:\n' \
                          '"give_content"\n' \
                          '"check_data"\n' \
                          '"get_data"\n' \
                          '"output_content"\n' \
                          'verb "give" count: 1\n' \
                          'verb "get" count: 1\n' \
                          '------------\n' \
                          'dirpath: ./django:\n' \
                          'total ".py" files count: 1\n' \
                          'All funcs names:\n' \
                          '"get_data"\n' \
                          '"check_data"\n' \
                          'verb "get" count: 1\n' \
                          '------------\n' \
                          'dirpath: ./flask:\n' \
                          'total ".py" files count: 1\n' \
                          'All funcs names:\n' \
                          '"give_content"\n' \
                          '"output_content"\n' \
                          'verb "give" count: 1\n' \
                          '------------\n' \
                          'total funcs names: 8\n' \
                          'unique funcs names: 4\n' \
                          'total verbs: 4\n' \
                          'unique verbs: 2\n' \
                          '"give" in 2 projects\n' \
                          '"get" in 2 projects\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            output_to_cli()
            self.assertEqual(fake_out.getvalue(), expected_result)

    def tearDown(self):
        shutil.rmtree('django')
        shutil.rmtree('flask')
        shutil.rmtree('myproject')
