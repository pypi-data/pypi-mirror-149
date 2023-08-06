import logging
from collections import namedtuple
from dataclasses import dataclass
import asyncio

from arps.core.observable_mixin import StochasticObservableMixin

TimeEvent = namedtuple('TimeEvent', 'value')


@dataclass
class EpochTime:
    epoch: int = 0
    valid: bool = True


class Clock(StochasticObservableMixin):

    def __init__(self, *, seconds_between_ticks: float) -> None:
        '''
        Initialize Clock instance

        Args:
        - seconds_between_ticks: seconds between ticks (this means
        that the clock will notify anyone listening to it after at
        least one second when update is called)
        '''
        super().__init__()

        self.seconds_between_ticks: float = seconds_between_ticks
        self._started: bool = False
        self._epoch_time: EpochTime = EpochTime()
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self) -> None:
        self._started = True
        self._epoch_time.valid = True
        self._epoch_time.epoch = 0

    @property
    def observer_interface(self):
        return self.add_listener, self.remove_listener

    @property
    def started(self) -> bool:
        return self._started

    @property
    def epoch_time(self) -> EpochTime:
        return self._epoch_time

    def reset(self) -> None:
        '''
        Reset clock
        '''
        self._started = False
        self._epoch_time.valid = False

    async def update(self) -> None:
        '''
        Update clock
        '''
        if not self.started:
            msg = 'Have you invoked Clock.start before running?'
            self.logger.warning(msg)
            print(msg)
            return

        await asyncio.sleep(self.seconds_between_ticks)
        self._epoch_time.epoch += 1
        self.logger.debug('Current epoch: %s', self.epoch_time.epoch)

        self.notify(TimeEvent(self._epoch_time.epoch))

    async def run(self) -> None:
        '''
        Start and tick the clock
        '''
        self.start()

        while True:
            try:
                await self.update()
            except asyncio.CancelledError:
                self.logger.info('epoch has been cancelled')
                await self.wait_for_notified_tasks()
                break
            except Exception as err:
                import traceback
                traceback.print_exc()
                msg = f'Error "{err}" while updating clock'
                print(msg)
                self.logger.warning(msg)

        await self.wait_for_notified_tasks()

        self.reset()

        self.logger.info('finishing clock instance')

    def __repr__(self):
        return f'Clock(seconds_between_ticks={self.seconds_between_ticks})'


def real_time_clock_factory() -> Clock:
    return Clock(seconds_between_ticks=1.0)


def simulator_clock_factory() -> Clock:
    return Clock(seconds_between_ticks=0.001)
