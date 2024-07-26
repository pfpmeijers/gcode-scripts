import os.path
from unittest import TestCase

from GCode import GCode
from utils.naming import camel_to_snake_case


class UnitTest(TestCase):

    path = '.'
    references_path = f'references'
    results_path = f'results'

    def __init__(self, *args):
        super().__init__(*args)
        self.name = camel_to_snake_case(self.__class__.__name__.replace('UnitTest', ''))

    def setUp(self):
        self.references_path = f'{self.path}/{self.references_path}/{self.name}'
        self.results_path = f'{self.path}/{self.results_path}/{self.name}'
        if not os.path.exists(self.references_path):
            os.mkdir(self.references_path)
        if not os.path.exists(self.results_path):
            os.mkdir(self.results_path)
        self.output_file_name = f'{self.id().split(".")[-1][5:]}.nc'
        self.output_file_path = f'{self.results_path}/{self.output_file_name}'
        self.output_file = open(self.output_file_path, 'w')
        self.gcode = GCode(self.output_file)

    def tearDown(self):
        self.output_file.close()
        self.assertEqualFile()

    def assertEqualFile(self, file_name: str = None):
        if file_name is None:
            file_name = self.output_file_name
        with open(f'{self.references_path}/{file_name}') as file:
            reference = file.read()
        with open(f'{self.results_path}/{file_name}') as file:
            result = file.read()
        self.assertEqual(reference, result)
