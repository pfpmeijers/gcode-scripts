from unittest import TestCase

from GCode import GCode
from utils.naming import camel_to_snake_case


class UnitTest(TestCase):

    path = '.'
    references_path = f'{path}/references'
    results_path = f'{path}/results'

    def __init__(self, *args):
        super().__init__(*args)
        self.name = camel_to_snake_case(self.__class__.__name__.replace('UnitTest', ''))

    def setUp(self):
        self.id()
        self.output_file_name = f'{self.name}-{self.id().split(".")[-1][5:]}.nc'
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
