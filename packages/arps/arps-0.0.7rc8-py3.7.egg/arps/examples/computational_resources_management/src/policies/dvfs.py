from arps.core.policy import (PeriodicPolicy,
                              ActionType)


class DVFSPolicy(PeriodicPolicy):

    def __init__(self, target_frequency, target_governor, predicate):
        self._predicate = predicate
        self._target_frequency = target_frequency
        self._target_governor = target_governor
        super().__init__()

    def _condition(self, host, event, epoch) -> bool:
        if not super()._condition(host, event, epoch):
            return False

        sensor_available = 'CPU' in host.sensors()
        if not sensor_available:
            return False

        frequency = host.read_sensor('CPU')
        condition_met = self._predicate(frequency)
        self.logger.info('current frequency {}, condition met {}'.format(frequency, condition_met))
        return condition_met

    def _action(self, host, event, epoch):
        self.logger.info(f'setting frequency to {self._target_frequency}, governor {self._target_governor}')
        governor, frequency = host.read_actuator('CPUFreq')
        if governor == self._target_governor:
            self.logger.info(f'already set to {governor}; do nothing')
            return (ActionType.result, True)

        host.modify_actuator('CPUFreq',
                             value=(self._target_governor, self._target_frequency),
                             identifier=host.identifier,
                             epoch=epoch)
        return (ActionType.result, True)


class PerformanceDVFSPolicy(DVFSPolicy):

    def __init__(self):
        super().__init__(target_frequency=2.9, target_governor='performance',
                         predicate=lambda frequency: frequency <= 50.0)


class PowersaveDVFSPolicy(DVFSPolicy):

    def __init__(self):
        super().__init__(target_frequency=0.9, target_governor='powersave',
                         predicate=lambda frequency: frequency > 80.0)
