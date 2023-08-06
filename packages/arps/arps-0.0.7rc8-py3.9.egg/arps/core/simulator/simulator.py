import asyncio
import logging
from contextlib import suppress
from typing import List, Dict, Generator, Iterable, Union

from arps.core.clock import TimeEvent
from arps.core.simulator.event_queue_loader import EventQueueLoader
from arps.core.simulator.sim_event import SimEvent
from arps.core.simulator.sim_event_scheduler import SimEventScheduler


class Simulator:
    '''
    Discrete event simulator
    '''

    def __init__(self, event_queue_loader: Union[Iterable, EventQueueLoader],
                 sim_event_scheduler: SimEventScheduler) -> None:
        '''
        Args:
        - event_queue_loader : event queue, not format defined yet
        - sim_event_scheduler: event scheduler
        '''
        self._has_events = True
        self._event_queue_loader = event_queue_loader
        self._event_gen = iter(self._event_queue_loader)
        self._current_events: List[SimEvent] = list()
        self._next_event_loader = self.load_next_events()
        self._next_event_loader.send(None)  # type: ignore
        self._event_scheduler = sim_event_scheduler
        self.logger = logging.getLogger(self.__class__.__name__)
        self._current_coro_events: Dict[int, Generator] = dict()
        self._finished_events: 'asyncio.Queue[SimEvent]' = asyncio.Queue()
        self.max_time = 0.0

    @property
    def finished(self):
        return not self._has_events

    def step(self, time_event: TimeEvent) -> None:
        '''
        Process events that are in the current epoch. Only process events if the epoch
        changed

        Return if there are more events in the event queue
        '''
        current_time = time_event.value
        self.logger.debug('running step at epoch time %s', current_time)

        events_available = self._next_event_loader.send(current_time)

        events_scheduled = self._event_scheduler.schedule(self._current_events, current_time)

        for event in events_scheduled:
            self.logger.debug('processing events at epoch time %s', current_time)
            if event.identifier not in self._current_coro_events:
                event_process = event.process()
                event_process.send(None)
                self._current_coro_events[event.identifier] = event_process

        for event_task_id, event_coro in self._current_coro_events.items():
            with suppress(StopIteration):
                event_coro.send(current_time)

        for event in self._current_events:
            if event.finished_time is not None:
                self._finished_events.put_nowait(event)
                del self._current_coro_events[event.identifier]

        self._current_events = [event for event in
                                self._current_events if event.finished_time is None]

        self._has_events = events_available or len(self._current_events) > 0

    def load_next_events(self) -> Generator[bool, int, None]:
        last = None
        has_events = True
        while True:
            current_time = yield has_events
            if last is not None and last.arrival_time == current_time:
                self._current_events.append(last)
                last = None

            if last is not None and last.arrival_time > current_time:
                continue

            while has_events:
                try:
                    result = next(self._event_gen)
                    if result.arrival_time > current_time:
                        last = result
                        break

                    if result.arrival_time == current_time:
                        self._current_events.append(result)
                except StopIteration:
                    has_events = False
