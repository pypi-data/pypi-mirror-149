import random

from arps.core.clock import EpochTime
from arps.core.simulator.resource import EvtType, TrackedValue
from arps.core.resources_table import ResourcesTable
from arps.core.simulator.sim_event import SimEvent
from arps.core.simulator.estimators_table import EstimatorsTable
from arps.core.simulator.event_factory import EventFactory


class CPUBoundedEvent(SimEvent):
    def __init__(self, identifier, arrival_time, remaining_time,
                 resources_table: ResourcesTable, estimators_table:
                 EstimatorsTable, load_size) -> None:
        self.load_size = load_size if load_size < 94 else load_size - 5
        super().__init__(identifier=identifier,
                         arrival_time=arrival_time,
                         remaining_time=remaining_time,
                         resources_table=resources_table,
                         estimators_table=estimators_table)
        self.acquired = False

    def main_task(self, epoch: EpochTime):
        resources = self.resources_table.resources_from_environment(environment_id=self.environment)
        cpu_instance = resources['CPU']


        if not self.acquired:
            if cpu_instance.value + self.load_size < 100:
                self.acquired = True
                cpu_instance.value = TrackedValue(cpu_instance.value + self.load_size, epoch, self.identifier, EvtType.des_main)
            else:
                return False

        energy_monitor = resources[('EnergyMonitor')]
        cpu_freq = resources['CPUFreq']
        governor, _ = cpu_freq.value
        if governor == 'performance':
            energy_monitor.value = TrackedValue(cpu_instance.value / 100 * 19 , epoch, self.identifier, EvtType.des_main)
        elif governor == 'powersave':
            energy_monitor.value = TrackedValue(random.random() * 5, epoch, self.identifier, EvtType.des_main)

        return True

    def pos(self, epoch: EpochTime):
        self.acquired = False
        resources = self.resources_table.resources_from_environment(environment_id=self.environment)
        cpu_instance = resources['CPU']
        cpu_instance.value = TrackedValue(cpu_instance.value - self.load_size, epoch, self.identifier, EvtType.des_pos)


class CPUBoundedEventFactory(EventFactory):
    def __call__(self, identifier, arrival_time, remaining_time, load_size) -> SimEvent:
        '''
        This loader is intended to work with traces that contain 6 columns to represent:
        Args:
        - identifier
        - remaining_time
        - start_time
        - load_size
        '''

        return self.create_sim_event(int(identifier),
                                     int(arrival_time), int(remaining_time), float(load_size))

    def create_sim_event(self, identifier: int, arrival_time: int,
                         remaining_time: int, load_size: float) -> SimEvent:
        '''
        Args
        - identifier: task global unique identifier
        - remaining_time: for how long the tasks execute
        - start_time: when the task starts
        - load_size: float value from 0 to 100
        '''
        return CPUBoundedEvent(identifier, int(arrival_time),
                               int(remaining_time), self.resources_table,
                               self.estimators_table, load_size)
