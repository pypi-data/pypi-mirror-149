import pathlib
import subprocess
import csv

from arps.core import select_resource_class
from arps.core.abstract_resource import AbstractResource
from arps.core.simulator.resource import Resource

from .computational_category import ComputationalCategory


class RealEstimateEnergy(AbstractResource):
    def __init__(self, *, environment_identifier, identifier):
        super().__init__(environment_identifier=environment_identifier,
                         identifier=identifier, category=ComputationalCategory.Energy)

    @property
    def value(self):
        collect_estimate()
        return parse()


def parse():
    if not pathlib.Path('result.csv').exists():
        print('file with the result is not ready')
        return 0.0

    with open('result.csv', 'r') as result:
        csv_file = csv.reader(result, delimiter=';')
        try:
            cpu = next(row for i, row in enumerate(csv_file) if row and 'The system baseline power' in row[0])[0]
        except StopIteration:
            print('row not found in the result.csv file')
            return 0.0
        else:
            cpu = cpu.split(':')[1].strip()
            cpu = cpu.split(' ')[0]
            return float(cpu)


def collect_estimate():
    p = subprocess.Popen(['powertop', '--csv=result.csv', '--time=1s'])
    try:
        p.wait(timeout=20)
    except subprocess.TimeoutExpired:
        pass


class FakeEstimateEnergy(Resource):
    def __init__(self, environment_identifier, identifier):
        super().__init__(environment_identifier=environment_identifier,
                         identifier=identifier, value=0.0,
                         category=ComputationalCategory.Energy)


EstimateEnergy = select_resource_class('EstimateEnergy', FakeEstimateEnergy, RealEstimateEnergy)
