'''Limitations: Works only on GNU/Linux

'''
import logging
import platform
import subprocess

import psutil

from arps.core import select_resource_class
from arps.core.abstract_resource import AbstractResource
from arps.core.simulator.resource import Resource

from .computational_category import ComputationalCategory

class RealCPU(AbstractResource):
    def __init__(self, *, environment_identifier, identifier):
        super().__init__(environment_identifier=environment_identifier,
                         identifier=identifier, category=ComputationalCategory.CPU)

    @property
    def value(self):
        return psutil.cpu_percent()


class RealCPUFreq(AbstractResource):
    def __init__(self, *, environment_identifier, identifier):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(environment_identifier=environment_identifier,
                         identifier=identifier, category=ComputationalCategory.CPUFreq)

    def modify_value(self, value, epoch, identifier, evt_type):
        if platform.system() == 'Windows':
            self.logger.warn('Running on Windows, this will do nothing')
            return

        target_frequency, governor = value

        self.logger.info('CPU Freq received:', target_frequency, governor, epoch, identifier, evt_type)

        frequency_params = f' -u {target_frequency}GHz '

        assert governor in ['powersave', 'performance']
        governor = f' -g {governor} '

        cpu_count = psutil.cpu_count() - 1

        command = f'for i in `seq {cpu_count}`; do cpufreq-set {frequency_params + governor} -c $i; done'

        self.logger.info('Executing {command_template}')
        status = subprocess.call(command, shell=True)
        self.logger.info(f'Result {status}')


class FakeCPU(Resource):
    def __init__(self, environment_identifier, identifier):
        utilization = 5.0 # a minimum utilization
        super().__init__(environment_identifier=environment_identifier,
                         identifier=identifier, initial_state=utilization,
                         category=ComputationalCategory.CPU)

class FakeCPUFreq(Resource):
    def __init__(self, environment_identifier, identifier):
        frequency = 2.9
        super().__init__(environment_identifier=environment_identifier,
                         identifier=identifier, initial_state=('performance', frequency),
                         category=ComputationalCategory.CPUFreq)

    def modify_value(self, value, epoch, identifier, evt_type):
        self.value = (value, epoch, identifier, evt_type)


CPU = select_resource_class('CPU', FakeCPU, RealCPU)
CPUFreq = select_resource_class('CPUFreq', FakeCPU, RealCPU)
